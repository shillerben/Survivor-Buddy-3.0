#include <VarSpeedServo.h>

/*
  AnalogReadSerial

  Reads an analog input on pin 0, prints the result to the Serial Monitor.
  Graphical representation is available using Serial Plotter (Tools > Serial Plotter menu).
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/AnalogReadSerial
*/

//Control and Feedback Pins
//regular 180 servos
int leftBasePin = 9; 
int rightBasePin = 10; 
int leftBaseFeedBack = A0; 
int rightBaseFeedBack = A1; 

//360 servo
int turnTablePin = 11;
int turnTableFeedBack  = A3;

//180 mini servo
int phoneMountPin =12 ;
int phoneMountFeedback = A4;

//Create VarSpeedServo objects 
VarSpeedServo leftBaseServo;
VarSpeedServo rightBaseServo;
VarSpeedServo turnTableServo;
VarSpeedServo phoneMountServo; 

typedef unsigned char u_char;
typedef unsigned short u_short;

enum Command : u_char {PITCH, YAW, ROLL, CLOSE, OPEN, PORTRAIT, LANDSCAPE, NOD, SHAKE, TILT};
/*
struct Command {
  static const u_char PITCH = 0;
  static const u_char YAW = 1;
  static const u_char ROLL = 2;
  static const u_char CLOSE = 3;
  static const u_char OPEN = 4;
  static const u_char PORTRAIT = 5;
  static const u_char LANDSCAPE = 6;
  static const u_char NOD = 7;
  static const u_char SHAKE = 8;
  static const u_char TILT = 9;
};
*/
              
// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  Serial.setTimeout(100);
}

// the loop routine runs over and over again forever:
void loop() {
  // read the data from USB
  u_char data;
  u_char val1;
  u_char val2;
  if (Serial.available() > 0) {
    data = Serial.read();

    switch(data) {
      case PITCH:
        val1 = Serial.read();
        set_pitch(val1);
        break;
      case YAW:
        val1 = Serial.read(); // higher byte
        val2 = Serial.read(); // lower byte
        set_yaw((val1 << 8) | val2);
        break;
      case ROLL:
        val1 = Serial.read();
        set_roll(val1);
        break;
      case CLOSE:
        close_();
        break;
      case OPEN:
        open_();
        break;
      case PORTRAIT:
        portrait();
        break;
      case LANDSCAPE:
        landscape();
        break;
      case NOD:
        nod();
        break;
      case SHAKE:
        shake();
        break;
      case TILT:
        tilt();
        break;
    }
    //Serial.print(data);
  }
  
  //delay(1);        // delay in between reads for stability
}

void set_pitch(u_char val) {
  Serial.print(val);
}

void set_yaw(u_short val) {
  Serial.print(val);
}

void set_roll(u_char val) {
  Serial.print(val);
}

void close_() {
  Serial.print(CLOSE);
}

void open_() {
  Serial.print(OPEN);
}

void portrait() {
  Serial.print(PORTRAIT);
}
              
void landscape() {
  Serial.print(LANDSCAPE);
}

void nod() {
  Serial.print(NOD);
}

void shake() {
  Serial.print(SHAKE);
}

void tilt() {
  Serial.print(TILT);
}
