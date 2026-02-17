"""
Firmware zegara Nixie Z5700M - wbudowany w aplikację
Źródło jest tutaj, nie trzeba osobnego pliku .ino
"""

FIRMWARE_VERSION = "1.0.0"

# Docelowa płytka - ATMega328P z MiniCore
# Jeśli masz standardowe Arduino Uno: zmień na "arduino:avr:uno"
BOARD_FQBN = "MiniCore:avr:328"

# Prędkość portu przy wgrywaniu
UPLOAD_BAUD = 115200

FIRMWARE_SOURCE = r"""
// AtMega328P TQFP pinout:
#define ButtonMIDDLE      3
#define ButtonRIGHT       4
#define SecondsRight      5
#define SecondsLeft       6
#define MinutesRight      7
#define CathodeC          8
#define PWM_DCDC          9
#define CathodeB          10
#define CathodeD          11
#define CathodeA          12
#define PointC            13
#define PointD             14
#define MinutesLeft        15
#define HoursRight         16
#define HoursLeft          17
#define ButtonLEFT          2

#include <Wire.h>
#include <DS3231.h>
#include <EEPROM.h>

// EEPROM LAYOUT:
// 0-1:  timeON (int)
// 2-3:  separator (int)
// 4:    dimEnabled (byte)
// 5:    dimStartHour (byte)
// 6:    dimStartMin (byte)
// 7:    dimEndHour (byte)
// 8:    dimEndMin (byte)
// 9:    dimBrightness (byte)
// 10:   schedEnabled (byte)
// 11:   schedOffHour (byte)
// 12:   schedOffMin (byte)
// 13:   schedOnHour (byte)
// 14:   schedOnMin (byte)

RTClib RTC;
DS3231 Clock;

int hour, minute, second, second2;
int jHou, kHou, jMin, kMin, jSec, kSec;
int timeON, timeOFF;
bool buttonMIDDLEState=LOW, buttonMIDDLELastState=LOW, buttonMIDDLERead=LOW;
int ASeparator, separator;
unsigned long debounceNow;
unsigned long debounceDelay = 200;

bool displayOff    = false;
int  dayBrightness = 100;

bool dimEnabled    = false;
byte dimStartHour  = 22, dimStartMin  = 0;
byte dimEndHour    = 8,  dimEndMin    = 0;
byte dimBrightness = 20;

bool schedEnabled  = false;
byte schedOffHour  = 23, schedOffMin  = 0;
byte schedOnHour   = 7,  schedOnMin   = 0;

String serialBuffer = "";

int brightnessToTimeON(int b) {
  return 10 + (int)(constrain(b,0,100) / 100.0 * 3990);
}

int timeONToBrightness(int t) {
  return (int)((constrain(t,10,4000) - 10) / 3990.0 * 100);
}

void saveSettings() {
  EEPROM.write(4,  dimEnabled   ? 1 : 0);
  EEPROM.write(5,  dimStartHour);
  EEPROM.write(6,  dimStartMin);
  EEPROM.write(7,  dimEndHour);
  EEPROM.write(8,  dimEndMin);
  EEPROM.write(9,  dimBrightness);
  EEPROM.write(10, schedEnabled ? 1 : 0);
  EEPROM.write(11, schedOffHour);
  EEPROM.write(12, schedOffMin);
  EEPROM.write(13, schedOnHour);
  EEPROM.write(14, schedOnMin);
}

void loadSettings() {
  dimEnabled    = EEPROM.read(4) == 1;
  dimStartHour  = EEPROM.read(5);
  dimStartMin   = EEPROM.read(6);
  dimEndHour    = EEPROM.read(7);
  dimEndMin     = EEPROM.read(8);
  dimBrightness = EEPROM.read(9);
  schedEnabled  = EEPROM.read(10) == 1;
  schedOffHour  = EEPROM.read(11);
  schedOffMin   = EEPROM.read(12);
  schedOnHour   = EEPROM.read(13);
  schedOnMin    = EEPROM.read(14);

  if (dimStartHour > 23) dimStartHour = 22;
  if (dimStartMin  > 59) dimStartMin  = 0;
  if (dimEndHour   > 23) dimEndHour   = 8;
  if (dimEndMin    > 59) dimEndMin    = 0;
  if (dimBrightness > 100) dimBrightness = 20;
  if (schedOffHour > 23) schedOffHour = 23;
  if (schedOffMin  > 59) schedOffMin  = 0;
  if (schedOnHour  > 23) schedOnHour  = 7;
  if (schedOnMin   > 59) schedOnMin   = 0;
}

bool timeInRange(byte nowH, byte nowM, byte startH, byte startM, byte endH, byte endM) {
  int now   = nowH * 60 + nowM;
  int start = startH * 60 + startM;
  int end   = endH * 60 + endM;
  if (start <= end) return (now >= start && now < end);
  return (now >= start || now < end);
}

void applyBrightness() {
  int b = dayBrightness;
  if (dimEnabled && timeInRange(hour, minute, dimStartHour, dimStartMin, dimEndHour, dimEndMin))
    b = dimBrightness;
  timeON  = brightnessToTimeON(b);
  timeOFF = 10000 / timeON;
  eeprom_write_block(&timeON, 0, 2);
}

void checkSchedule() {
  if (!schedEnabled) {
    if (displayOff) { displayOff = false; digitalWrite(PWM_DCDC, HIGH); }
    return;
  }
  bool off = timeInRange(hour, minute, schedOffHour, schedOffMin, schedOnHour, schedOnMin);
  if (off && !displayOff)      { displayOff=true;  off_all(); digitalWrite(PWM_DCDC, LOW); }
  else if (!off && displayOff) { displayOff=false; digitalWrite(PWM_DCDC, HIGH); delay(50); }
}

void processCommand(String cmd) {
  cmd.trim();

  if (cmd.startsWith("SET_TIME:")) {
    String t=cmd.substring(9);
    int h=t.substring(0,2).toInt(), m=t.substring(3,5).toInt(), s=t.substring(6,8).toInt();
    if(h<=23&&m<=59&&s<=59){Clock.setHour(h);Clock.setMinute(m);Clock.setSecond(s);Serial.println("OK:TIME_SET");}
    else Serial.println("ERR:INVALID_TIME");
  }
  else if (cmd.startsWith("SET_BRIGHTNESS:")) {
    int b=cmd.substring(15).toInt();
    if(b>=0&&b<=100){dayBrightness=b;applyBrightness();Serial.println("OK:BRIGHTNESS_SET");}
    else Serial.println("ERR:INVALID_BRIGHTNESS");
  }
  else if (cmd.startsWith("SET_DIM:")) {
    String p=cmd.substring(8);
    int c1=p.indexOf(','), c2=p.lastIndexOf(',');
    if(c1>0&&c2>c1){
      String s1=p.substring(0,c1), s2=p.substring(c1+1,c2);
      int bri=p.substring(c2+1).toInt();
      byte sh=s1.substring(0,2).toInt(), sm=s1.substring(3,5).toInt();
      byte eh=s2.substring(0,2).toInt(), em=s2.substring(3,5).toInt();
      if(sh<=23&&sm<=59&&eh<=23&&em<=59&&bri>=0&&bri<=100){
        dimEnabled=true;dimStartHour=sh;dimStartMin=sm;dimEndHour=eh;dimEndMin=em;dimBrightness=bri;
        saveSettings();applyBrightness();Serial.println("OK:DIM_SET");
      } else Serial.println("ERR:INVALID_DIM_PARAMS");
    } else Serial.println("ERR:INVALID_DIM_FORMAT");
  }
  else if (cmd=="DIM_DISABLE") {
    dimEnabled=false;saveSettings();applyBrightness();Serial.println("OK:DIM_DISABLED");
  }
  else if (cmd.startsWith("SET_SCHEDULE:")) {
    String p=cmd.substring(13);
    int c1=p.indexOf(',');
    if(c1>0){
      String so=p.substring(0,c1), sn=p.substring(c1+1);
      byte oh=so.substring(0,2).toInt(), om=so.substring(3,5).toInt();
      byte nh=sn.substring(0,2).toInt(), nm=sn.substring(3,5).toInt();
      if(oh<=23&&om<=59&&nh<=23&&nm<=59){
        schedEnabled=true;schedOffHour=oh;schedOffMin=om;schedOnHour=nh;schedOnMin=nm;
        saveSettings();Serial.println("OK:SCHEDULE_SET");
      } else Serial.println("ERR:INVALID_SCHEDULE_PARAMS");
    } else Serial.println("ERR:INVALID_SCHEDULE_FORMAT");
  }
  else if (cmd=="SCHEDULE_DISABLE") {
    schedEnabled=false;saveSettings();
    if(displayOff){displayOff=false;digitalWrite(PWM_DCDC,HIGH);delay(50);}
    Serial.println("OK:SCHEDULE_DISABLED");
  }
  else if (cmd=="GET_STATUS") {
    Serial.print("TIME:");Serial.print(hour);Serial.print(":");
    if(minute<10)Serial.print("0");Serial.print(minute);Serial.print(":");
    if(second<10)Serial.print("0");Serial.println(second);
    Serial.print("BRIGHTNESS:");Serial.println(dayBrightness);
    Serial.print("DIM:");Serial.print(dimEnabled?"1":"0");Serial.print(",");
    Serial.print(dimStartHour);Serial.print(":");Serial.print(dimStartMin);Serial.print(",");
    Serial.print(dimEndHour);Serial.print(":");Serial.print(dimEndMin);Serial.print(",");Serial.println(dimBrightness);
    Serial.print("SCHEDULE:");Serial.print(schedEnabled?"1":"0");Serial.print(",");
    Serial.print(schedOffHour);Serial.print(":");Serial.print(schedOffMin);Serial.print(",");
    Serial.print(schedOnHour);Serial.print(":");Serial.println(schedOnMin);
  }
  else {
    Serial.print("ERR:UNKNOWN:");Serial.println(cmd);
  }
}

void handleSerial() {
  while(Serial.available()){
    char c=Serial.read();
    if(c=='\n'||c=='\r'){
      if(serialBuffer.length()>0){processCommand(serialBuffer);serialBuffer="";}
    } else {
      serialBuffer+=c;
      if(serialBuffer.length()>64) serialBuffer="";
    }
  }
}

void setup() {
  pinMode(PointC,OUTPUT);pinMode(PointD,OUTPUT);
  pinMode(MinutesLeft,OUTPUT);pinMode(MinutesRight,OUTPUT);
  pinMode(SecondsLeft,OUTPUT);pinMode(SecondsRight,OUTPUT);
  pinMode(HoursLeft,OUTPUT);pinMode(HoursRight,OUTPUT);
  pinMode(CathodeA,OUTPUT);pinMode(CathodeB,OUTPUT);
  pinMode(CathodeC,OUTPUT);pinMode(CathodeD,OUTPUT);
  pinMode(PWM_DCDC,OUTPUT);
  pinMode(ButtonLEFT,INPUT);pinMode(ButtonMIDDLE,INPUT);pinMode(ButtonRIGHT,INPUT);

  digitalWrite(PointC,LOW);digitalWrite(PointD,LOW);digitalWrite(PWM_DCDC,LOW);
  digitalWrite(CathodeA,HIGH);digitalWrite(CathodeB,HIGH);
  digitalWrite(CathodeC,HIGH);digitalWrite(CathodeD,HIGH);
  digitalWrite(SecondsLeft,LOW);digitalWrite(SecondsRight,LOW);
  digitalWrite(MinutesLeft,LOW);digitalWrite(MinutesRight,LOW);
  digitalWrite(HoursLeft,LOW);digitalWrite(HoursRight,LOW);

  delay(100);digitalWrite(PWM_DCDC,HIGH);delay(100);
  digitalWrite(PWM_DCDC,LOW);delay(100);digitalWrite(PWM_DCDC,HIGH);
  depoison(70);

  Wire.begin();
  Serial.begin(9600);

  eeprom_read_block(&timeON,0,2);
  eeprom_read_block(&separator,2,2);
  if(timeON<10||timeON>4000){timeON=2000;eeprom_write_block(&timeON,0,2);}
  dayBrightness=timeONToBrightness(timeON);
  timeOFF=10000/timeON;
  loadSettings();
  Serial.println("OK:NIXIE_READY");
}

void loop() {
  handleSerial();
  second2=second;
  DateTime now=RTC.now();
  hour=now.hour();minute=now.minute();second=now.second();
  jSec=second/10;kSec=second%10;
  jMin=minute/10;kMin=minute%10;
  jHou=hour/10;  kHou=hour%10;

  if(second!=second2){checkSchedule();applyBrightness();}
  if(minute==0&&(second==0||second==1||second==2)){depoison(150);}

  if(!displayOff){
    on_number(HoursLeft,jHou);   point(separator);delayMicroseconds(timeON);off_all();delayMicroseconds(timeOFF);
    on_number(HoursRight,kHou);  point(separator);delayMicroseconds(timeON);off_all();delayMicroseconds(timeOFF);
    on_number(MinutesLeft,jMin); point(separator);delayMicroseconds(timeON);off_all();delayMicroseconds(timeOFF);
    on_number(MinutesRight,kMin);point(separator);delayMicroseconds(timeON);off_all();delayMicroseconds(timeOFF);
  }

  if(digitalRead(ButtonMIDDLE)==LOW){buttonMIDDLERead=HIGH;}else{buttonMIDDLERead=LOW;}
  if(buttonMIDDLERead!=buttonMIDDLELastState){debounceNow=millis();}
  if((millis()-debounceNow)>debounceDelay){
    if(buttonMIDDLERead!=buttonMIDDLEState){
      buttonMIDDLEState=buttonMIDDLERead;
      if(buttonMIDDLERead==HIGH){separator++;if(separator>=5){separator=0;}eeprom_write_block(&separator,2,2);}}}
  buttonMIDDLELastState=buttonMIDDLERead;

  if(digitalRead(ButtonLEFT)==LOW&&digitalRead(ButtonMIDDLE)==LOW){
    if(hour<23){Clock.setHour(hour+1);delay(400);}else{Clock.setHour(0);delay(400);}
  }
  if(digitalRead(ButtonRIGHT)==LOW&&digitalRead(ButtonMIDDLE)==LOW){
    if(minute<59){Clock.setMinute(minute+1);Clock.setSecond(0);delay(300);}else{Clock.setMinute(0);delay(300);}
  }
  if(digitalRead(ButtonLEFT)==LOW&&digitalRead(ButtonRIGHT)==LOW){
    timeON=timeON/1.01;if(timeON<=10){timeON=4000;}
    dayBrightness=timeONToBrightness(timeON);timeOFF=10000/timeON;
    eeprom_write_block(&timeON,0,2);
  }
}

void on_number(int row, int nixie) {
  switch(nixie){
    case 0:digitalWrite(CathodeA,HIGH);digitalWrite(CathodeB,HIGH);digitalWrite(CathodeC,LOW); digitalWrite(CathodeD,LOW); break;
    case 1:digitalWrite(CathodeA,LOW); digitalWrite(CathodeB,LOW); digitalWrite(CathodeC,LOW); digitalWrite(CathodeD,LOW); break;
    case 2:digitalWrite(CathodeA,HIGH);digitalWrite(CathodeB,LOW); digitalWrite(CathodeC,LOW); digitalWrite(CathodeD,LOW); break;
    case 3:digitalWrite(CathodeA,HIGH);digitalWrite(CathodeB,LOW); digitalWrite(CathodeC,HIGH);digitalWrite(CathodeD,LOW); break;
    case 4:digitalWrite(CathodeA,LOW); digitalWrite(CathodeB,LOW); digitalWrite(CathodeC,HIGH);digitalWrite(CathodeD,LOW); break;
    case 5:digitalWrite(CathodeA,LOW); digitalWrite(CathodeB,HIGH);digitalWrite(CathodeC,LOW); digitalWrite(CathodeD,LOW); break;
    case 6:digitalWrite(CathodeA,LOW); digitalWrite(CathodeB,LOW); digitalWrite(CathodeC,LOW); digitalWrite(CathodeD,HIGH);break;
    case 7:digitalWrite(CathodeA,HIGH);digitalWrite(CathodeB,LOW); digitalWrite(CathodeC,LOW); digitalWrite(CathodeD,HIGH);break;
    case 8:digitalWrite(CathodeA,LOW); digitalWrite(CathodeB,HIGH);digitalWrite(CathodeC,HIGH);digitalWrite(CathodeD,LOW); break;
    case 9:digitalWrite(CathodeA,HIGH);digitalWrite(CathodeB,HIGH);digitalWrite(CathodeC,HIGH);digitalWrite(CathodeD,LOW); break;
  }
  digitalWrite(row,HIGH);
}

void off_all(){
  digitalWrite(MinutesLeft,LOW);digitalWrite(MinutesRight,LOW);
  digitalWrite(HoursLeft,LOW);digitalWrite(HoursRight,LOW);
  digitalWrite(PointC,LOW);digitalWrite(PointD,LOW);
  digitalWrite(CathodeA,HIGH);digitalWrite(CathodeB,HIGH);
  digitalWrite(CathodeC,HIGH);digitalWrite(CathodeD,HIGH);
}

void depoison(int t){
  int d=0;
  while(d<10){digitalWrite(PointC,HIGH);digitalWrite(PointD,HIGH);on_number(HoursLeft,d);  delay(t);off_all();d++;}d=0;
  while(d<10){digitalWrite(PointC,HIGH);digitalWrite(PointD,HIGH);on_number(HoursRight,d); delay(t);off_all();d++;}d=0;
  while(d<10){digitalWrite(PointC,HIGH);digitalWrite(PointD,HIGH);on_number(MinutesLeft,d);delay(t);off_all();d++;}d=0;
  while(d<10){digitalWrite(PointC,HIGH);digitalWrite(PointD,HIGH);on_number(MinutesRight,d);delay(t);off_all();d++;}d=0;
}

void point(int p){
  switch(p){
    case 0:digitalWrite(PointC,LOW);digitalWrite(PointD,LOW);break;
    case 1:digitalWrite(PointC,HIGH);digitalWrite(PointD,HIGH);break;
    case 2:digitalWrite(PointC,second%2);digitalWrite(PointD,!digitalRead(PointC));break;
    case 3:digitalWrite(PointC,second%2);digitalWrite(PointD,second%2);break;
    case 4:digitalWrite(PointC,HIGH);digitalWrite(PointD,HIGH);
    case 5:
      if(digitalRead(HoursLeft)==HIGH)  ASeparator=0;
      if(digitalRead(HoursRight)==HIGH) ASeparator=1;
      if(digitalRead(MinutesLeft)==HIGH)ASeparator=2;
      if(digitalRead(MinutesRight)==HIGH)ASeparator=3;
      if(digitalRead(SecondsLeft)==HIGH)ASeparator=4;
      if(digitalRead(SecondsRight)==HIGH)ASeparator=5;
      switch(ASeparator){
        case 0:digitalWrite(PointC,LOW); digitalWrite(PointD,LOW); break;
        case 1:digitalWrite(PointC,LOW); digitalWrite(PointD,HIGH);break;
        case 2:digitalWrite(PointC,HIGH);digitalWrite(PointD,LOW); break;
        case 3:digitalWrite(PointC,LOW); digitalWrite(PointD,HIGH);break;
        case 4:digitalWrite(PointC,HIGH);digitalWrite(PointD,LOW); break;
        case 5:digitalWrite(PointC,LOW); digitalWrite(PointD,LOW); break;
      }break;
  }
}
"""
