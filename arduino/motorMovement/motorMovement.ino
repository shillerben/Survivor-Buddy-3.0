#include <VarSpeedServo.h>

//Control and Feedback Pins
//regular 180 servos
int leftBasePin = 9; 
int rightBasePin = 10; 
int leftBaseFeedback = A0; 
int rightBaseFeedback = A1; 

//360 servo
int turnTablePin = 3;
int turnTableFeedback  = 11;

//180 mini servo
int phoneMountPin =6;
int phoneMountFeedback = A4;

int ledPin = 2;

// Position constants
const int RIGHT_BASE_DOWN = 40;
const int RIGHT_BASE_UP = 125;
const int LEFT_BASE_DOWN = 150;
const int LEFT_BASE_UP = 65;
const int PHONEMOUNT_LANDSCAPE = 7;
const int PHONEMOUNT_PORTRAIT = 115;
const int PHONEMOUNT_TILT = 60;

// Feedback constants
const int RIGHT_BASE_FB_DOWN = 186;
const int RIGHT_BASE_FB_UP = 369;
const int LEFT_BASE_FB_DOWN = 415;
const int LEFT_BASE_FB_UP = 235;
const int PHONEMOUNT_FB_PORTRAIT = 0;
const int PHONEMOUNT_FB_LANDSCAPE = 0;
const int TABLETOP_LEFT = 0;
const int TABLETOP_RIGHT = 0;

//Create VarSpeedServo objects 
VarSpeedServo leftBaseServo;
VarSpeedServo rightBaseServo;
VarSpeedServo turnTableServo;
VarSpeedServo phoneMountServo; 

//Serial Data
unsigned char serialData;

enum Command {PITCH, YAW, ROLL, CLOSE, OPEN, PORTRAIT, 
              LANDSCAPE, NOD, SHAKE, TILT};

/*******************************************************************/
/*Phone Mount Functions*/
void portrait(){ //phoneMountServo moves phone to portrait position
    phoneMountServo.write(PHONEMOUNT_PORTRAIT, 40, true);
}

void landscape(){ //phoneMountServo moves phone to landscape position
    phoneMountServo.write(PHONEMOUNT_LANDSCAPE, 40, true);
}

void tiltPortrait(){ //phoneMountServo moves phone to tilted position
    phoneMountServo.write(PHONEMOUNT_TILT, 60, true);
    delay(500);
    phoneMountServo.write(PHONEMOUNT_PORTRAIT, 60, true);
}

void tiltLandscape(){ //phoneMountServo moves phone to tilted position
    phoneMountServo.write(PHONEMOUNT_TILT, 60, true);
    delay(500);
    phoneMountServo.write(PHONEMOUNT_LANDSCAPE, 60, true);
}

/*
 * Get current position of Phone Mount Servo
*/
int getPositionPM(){
  int potVal = analogRead(phoneMountFeedback);
  return map(potVal, PHONEMOUNT_FB_PORTRAIT, PHONEMOUNT_FB_LANDSCAPE, 0, 90);
}
/*******************************************************************/
/*Base Motor Functions*/
/*
 * Get current position of Base Servos
*/
int getPositionBM(){
//  int potValLeft = analogRead(leftBaseFeedback);
//  int leftAngle = map(potValLeft, LEFT_BASE_FB_DOWN, LEFT_BASE_FB_UP, 0, 90);
  int potValRight = analogRead(rightBaseFeedback);
  int rightAngle = map(potValRight, RIGHT_BASE_FB_DOWN, RIGHT_BASE_FB_UP, 0, 90);
  return rightAngle;
}

// 360 parallax constants
const int unitsFC = 360; // 360 degrees in a circle
const int dcMin = 29;
const int dcMax = 971;
const int dutyScale = 1;
// not constants, but don't want to have to declare them a lot
unsigned long tCycle, tHigh, tLow, dc;
unsigned int theta;

int getPositionTabletop(){
  int tCycle = 0;
  int tHigh, tLow, theta, dc;
  while (1) {
    tHigh = pulseIn(turnTableFeedback, HIGH);
    tLow = pulseIn(turnTableFeedback, LOW);
    tCycle = tHigh + tLow;
    Serial.print("tHigh: ");
    Serial.println(tHigh);
    Serial.print("tLow: ");
    Serial.println(tLow);
    Serial.print("tCycle: ");
    Serial.println(tCycle);
    if ((tCycle > 1000) && (tCycle < 1200)) {
      break;
    }
  }
  dc = (dutyScale * tHigh) / tCycle;
  theta = (unitsFC - 1) - ((dc - dcMin) * unitsFC) / (dcMax - dcMin + 1);
  if (theta < 0) {
    theta = 0;
  }
  else if (theta > (unitsFC - 1)) {
    theta = unitsFC - 1;
  }
  return theta;
}

void close_(){
  // front, portrait, then down
}

void up(){
  leftBaseServo.write(LEFT_BASE_UP, 40);
  rightBaseServo.write(RIGHT_BASE_UP, 40);
  leftBaseServo.wait();
  rightBaseServo.wait();
}
void down(){
  leftBaseServo.write(LEFT_BASE_DOWN, 40);
  rightBaseServo.write(RIGHT_BASE_DOWN, 40);
  leftBaseServo.wait();
  rightBaseServo.wait();
}
void nod(){
  //up down, arm nods twice
  leftBaseServo.write(LEFT_BASE_UP, 60);
  rightBaseServo.write(RIGHT_BASE_UP, 60);
  leftBaseServo.wait();
  rightBaseServo.wait();
  delay(100);
  leftBaseServo.write(70, 60);
  rightBaseServo.write(70, 60);
  leftBaseServo.wait();
  rightBaseServo.wait();
  delay(100);
  leftBaseServo.write(LEFT_BASE_UP, 60);
  rightBaseServo.write(RIGHT_BASE_UP, 60);
  leftBaseServo.wait();
  rightBaseServo.wait();
  delay(100);
  leftBaseServo.write(70, 60);
  rightBaseServo.write(70, 60);
  leftBaseServo.wait();
  rightBaseServo.wait();
  delay(100);
  leftBaseServo.write(LEFT_BASE_UP, 60);
  rightBaseServo.write(RIGHT_BASE_UP, 60);
  leftBaseServo.wait();
  rightBaseServo.wait();
}
/*******************************************************************/
/*Turn Table Motor Functions*/
void shake(){
  //move left and right
}

/*******************************************************************/

/*
 * Zero all motors
 * Return all motors to 0 pos
 * Phonemount to portrait mode (90 pos)
*/
void homeServos(){
  //Reset all servos to position 0
  close_(); 
}
/*Emergency Shut Down*/
void emergencyShutdown(){
  //stop all motor movement. will need to unplug and plug back in to move again
  while(true) {}
}

/*Normal Shut Down*/
void shutdown(){
  //need to make sure all other motors are in correct postion to close
//close arm all the way
}

void test() {
  /*
  Serial.println("TESTING...");
  up();
  Serial.println(getPositionTabletop());
  */
//  tHigh = pulseIn(turnTableFeedback, HIGH);
//  Serial.println(tHigh);
  turnTableServo.write(90);
  delay(1000);
  turnTableServo.write(115);
  delay(50);
  turnTableServo.write(65);
  delay(50);
  turnTableServo.write(90);
}

/*******************************************************************/
void setup() {
  Serial.begin(9600);

  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  // feedback pins
  pinMode(leftBaseFeedback, INPUT);
  pinMode(rightBaseFeedback, INPUT);
  pinMode(turnTableFeedback, INPUT);
  pinMode(phoneMountFeedback, INPUT);
  
  // attaches the servo on pin to the servo object
  leftBaseServo.attach(leftBasePin);  
  leftBaseServo.write(LEFT_BASE_UP);
  rightBaseServo.attach(rightBasePin);
  rightBaseServo.write(RIGHT_BASE_UP);
  turnTableServo.attach(turnTablePin);
  phoneMountServo.attach(phoneMountPin);
  phoneMountServo.write(PHONEMOUNT_PORTRAIT);
}

void loop() {
  //test();
  
  if (Serial.available() > 0) {//serial is reading stuff 
    serialData = Serial.read(); 

    if(serialData == 0x03){ // close 
      down();
    }
    //phone mount serials ****************************************
    else if (serialData == 0x04){ // open
      up();
    }
    else if(serialData == 0x05){ // portrait
      portrait();
    }
    else if (serialData == 0x06){ // landscape
      landscape();
    } 
    else if(serialData == 0x07){ // nod
      nod();
    }
    //base motor serials ****************************************
    else if (serialData == 0x08){ // shake
      shake();
    }
    else if(serialData == 0x09){ // tilt
      tiltPortrait();
    }
  }
} //end loop
