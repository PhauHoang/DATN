#include <Servo.h>
Servo servo1;
Servo servo2;
#define CB1 11
#define CB2 10
#define CB3 9

#define BT  4
#define thu   180
#define gat   130
#define BAT   1
#define TAT   0
int time_gat = 3000;
String dataa = "";
char mang[20];
char *token1, *token2, *token3, *token4;
int lan = 0, xong = 0, i = 0;
int loai = 0, modee = 0;
int hong = 0, khac = 0, dat = 0, st = 0, g1 = 0, g2 = 0, chup = 0, bt = 0;
unsigned long int time_gui = 0;
//*****************************************************************************************//
void setup() {
  Serial.begin(9600);
  pinMode(CB1, INPUT_PULLUP);
  pinMode(CB2, INPUT_PULLUP);
  pinMode(CB3, INPUT_PULLUP);
  pinMode(BT, OUTPUT);
  digitalWrite(BT, TAT);
  servo1.attach(8);
  servo2.attach(7);
  servo1.write(thu);
  servo2.write(thu);
  gui_du_lieu2();
  delay(500);
}
//*****************************************************************************************//
void loop() {
  stopp();
  gui_du_lieu2();
  if (modee == 0) {
    Auto();
  }
  else {
    Manual();
  }

}
//*****************************************************************************************//
void serialEvent() {
  while (Serial.available()) {
    dataa = Serial.readStringUntil('\n');
    dataa.toCharArray(mang, 20);
    token1 = strtok(mang, "|");
    token2 = strtok(NULL, "|");
    String st1(token1);
    String st2(token2);
    if (st1 == "a") {
      modee = st2.toInt();
      st = 0;
      digitalWrite(BT, TAT);
      bt = 0;
      g1 = 0;
      g2 = 0;
    }
    if (st1 == "b") st = st2.toInt();
    if (st1 == "c") g1 = st2.toInt();
    if (st1 == "d") g2 = st2.toInt();
    if (st1 == "e") bt = st2.toInt();
    if (st1 == "f") loai = st2.toInt();
    if (st1 == "g") xong = st2.toInt();
  }
}
//*****************************************************************************************//
void Auto() {
  if (st == 1) {
    digitalWrite(BT, BAT);
    if (digitalRead(CB1) == 0) {
      if(lan == 0){ 
        delay(100);
        digitalWrite(BT, TAT);
        delay(500);
        chup = 1;
        gui_du_lieu();
        chup = 0;
        while(xong == 0){
          serialEvent();
          chup = 0;
          stopp();
        }
        digitalWrite(BT, BAT);
        while (digitalRead(CB1) == 0){
          delay(100);
          stopp();
        }
        delay(400);
      } 
    }
    if (loai == 0) {
      if (digitalRead(CB2) == 0) {
        servo1.write(gat);
        delay(time_gat);
        servo1.write(thu);
        hong++;
        lan = 0;
        delay(200);
        gui_du_lieu();
      }
    }
    else if (loai == 2) {
      if (digitalRead(CB3) == 0) {
        servo2.write(gat);
        delay(time_gat);
        servo2.write(thu);
        khac++;
        lan = 0;
        delay(200);
        gui_du_lieu();
      }
    }
    else {
      if (digitalRead(CB3) == 0) {
        while (digitalRead(CB3) == 0) {
          digitalWrite(BT, BAT);
          delay(100);
          stopp();
        }
        dat++;
        lan = 0;
        gui_du_lieu();
      }
    }
  }
}

//*****************************************************************************************//
void Manual() {
  if (st == 1) {
    if (g1 == 0) {
      servo1.write(thu);
    }
    else {
      servo1.write(gat);
    }

    if (g2 == 0) {
      servo2.write(thu);
    }
    else {
      servo2.write(gat);
    }

    if (bt == 0) {
      digitalWrite(BT, TAT);
    }
    else {
      digitalWrite(BT, BAT);
    }
  }
}
//*****************************************************************************************//
void gui_du_lieu() {
    Serial.print(modee);
    Serial.print("|");
    Serial.print(st);
    Serial.print("|");
    Serial.print(chup);
    Serial.print("|");
    Serial.print(khac);
    Serial.print("|");
    Serial.print(hong);
    Serial.print("|");
    Serial.println(dat);
}
//*****************************************************************************************//
void gui_du_lieu2() {
  if (millis() - time_gui >= 500) {
    Serial.print(modee);
    Serial.print("|");
    Serial.print(st);
    Serial.print("|");
    Serial.print(chup);
    Serial.print("|");
    Serial.print(khac);
    Serial.print("|");
    Serial.print(hong);
    Serial.print("|");
    Serial.println(dat);
    time_gui = millis();
    //0|1|1|2|2|2
  }
}
//*****************************************************************************************//
void stopp() {
  while (st == 2) {
    serialEvent();
    digitalWrite(BT, TAT);
    gui_du_lieu2();
  }
}
