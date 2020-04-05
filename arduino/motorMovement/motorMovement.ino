#include <VarSpeedServo.h>

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

//Serial Data
char serialData;

enum Command {PITCH, YAW, ROLL, CLOSE, OPEN, PORTRAIT, 
              LANDSCAPE, NOD, SHAKE, TILT};

/* put your setup code here, to run once: */
void setup() {
  Serial.begin(9600);
  
  // attaches the servo on pin to the servo object
  leftBaseServo.attach(leftBasePin, 0, 90);  
  rightBaseServo.attach(rightBasePin);
  turnTableServo.attach(turnTablePin);
  phoneMountServo.attach(phoneMountPin);
}

/*******************************************************************/
/*Phone Mount Functions*/
void portrait(){ //phoneMountServo moves phone to portrait position
    phoneMountServo.write(90);
    delay(1000); 
}
void landscape(){ //phoneMountServo moves phone to landscape position
    phoneMountServo.write(180);
    delay(1000); 
} 
void tilt(){ //phoneMountServo moves phone to tilted position
    phoneMountServo.write(135);
    delay(1000);
}
/*
 * Get current position of Phone Mount Servo
*/
int getPositionPM(){
  int anglePos;
  int potVal = analogRead(phoneMountFeedback);

  if ( potVal >= 606){
    anglePos = 180;
  }
  else if(potVal >= 590){
    anglePos = 175;
  }
  else if (potVal >= 575){
    anglePos = 170; 
  }
  else if(potVal >= 559){
    anglePos = 165;
  }
  else if (potVal >= 543){
    anglePos = 160; 
  }
  else if(potVal >= 529){
    anglePos = 155;
  }
  else if (potVal >= 514){
    anglePos = 150; 
  }
  else if(potVal >= 498){
    anglePos = 145;
  }
  else if (potVal >= 484){
    anglePos = 140; 
  }
  else if(potVal >= 468){
    anglePos = 135;
  }
  else if (potVal >= 453){
    anglePos = 130; 
  }
  else if(potVal >= 437){
    anglePos = 125;
  }
  else if (potVal >= 423){
    anglePos = 120; 
  }
  else if(potVal >= 406){
    anglePos = 115;
  }
  else if (potVal >= 391){
    anglePos = 110; 
  }
  else if(potVal >= 376){
    anglePos = 105;
  }
  else if (potVal >= 360){
    anglePos = 100; 
  }
  else if(potVal >= 344){
    anglePos = 95;
  }
  else if (potVal >= 330){
    anglePos = 90; 
  }
  else if(potVal >= 313){
    anglePos = 85;
  }
  else if (potVal >= 298){
    anglePos = 80; 
  }
  else if(potVal >= 282){
    anglePos = 75;
  }
  else if (potVal >= 266){
    anglePos = 70; 
  }
  else if(potVal >= 251){
    anglePos = 65;
  }
  else if (potVal >= 236){
    anglePos = 60; 
  }
  else if(potVal >= 221){
    anglePos = 55;
  }
  else if (potVal >= 204){
    anglePos = 50; 
  }
  else if(potVal >= 191){
    anglePos = 45;
  }
  else if (potVal >= 174){
    anglePos = 40; 
  }
  else if(potVal >= 158){
    anglePos = 35;
  }
  else if (potVal >= 143){
    anglePos = 30; 
  }
  else if(potVal >= 129){
    anglePos = 25;
  }
  else if (potVal >= 112){
    anglePos = 20; 
  }
  else if(potVal >= 98){
    anglePos = 15;
  }
  else if (potVal >= 82){
    anglePos = 10; 
  }
  else if(potVal >= 68){
    anglePos = 5;
  }
  else {
    anglePos = 0; 
  }
return anglePos;
}
/*******************************************************************/
/*Base Motor Functions*/
/*
 * Get current position of Base Servos
*/
int getPositionBM(){ //left base motor and right base motor
//decided to only get left base motor pot values
//as pot intervals vary from left and right motor
//but want them both to be at the same angle at all times
//assign same pos to both motors
//if potvalleft && potvalright, cant gurantee if, else always be 0
  int anglePos;
  int potValLeft = analogRead(leftBaseFeedBack);
  int potValRight = analogRead(rightBaseFeedBack);

  if ( potValLeft >= 467){
    anglePos = 180;
  }
  else if(potValLeft >= 458){
    anglePos = 175;
  }
  else if (potValLeft >= 448){
    anglePos = 170; 
  }
  else if(potValLeft >= 438){
    anglePos = 165;
  }
  else if (potValLeft >= 428){
    anglePos = 160; 
  }
  else if(potValLeft >= 419){
    anglePos = 155;
  }
  else if (potValLeft >= 408){
    anglePos = 150; 
  }
  else if(potValLeft >= 399){
    anglePos = 145;
  }
  else if (potValLeft >= 388){
    anglePos = 140; 
  }
  else if(potValLeft >= 377){
    anglePos = 135;
  }
  else if (potValLeft >= 367){
    anglePos = 130; 
  }
  else if(potValLeft >= 357){
    anglePos = 125;
  }
  else if (potValLeft >= 347 ){
    anglePos = 120; 
  }
  else if(potValLeft >= 336){
    anglePos = 115;
  }
  else if (potValLeft >= 326){
    anglePos = 110; 
  }
  else if(potValLeft >= 316){
    anglePos = 105;
  }
  else if (potValLeft >=305 ){
    anglePos = 100; 
  }
  else if(potValLeft >=296 ){
    anglePos = 95;
  }
  else if (potValLeft >= 286){
    anglePos = 90; 
  }
  else if(potValLeft >=273 ){
    anglePos = 85;
  }
  else if (potValLeft >=264 ){
    anglePos = 80; 
  }
  else if(potValLeft >=252 ){
    anglePos = 75;
  }
  else if (potValLeft >=242 ){
    anglePos = 70; 
  }
  else if(potValLeft >=232 ){
    anglePos = 65;
  }
  else if (potValLeft >= 222){
    anglePos = 60; 
  }
  else if(potValLeft >= 209){
    anglePos = 55;
  }
  else if (potValLeft >= 198){
    anglePos = 50; 
  }
  else if(potValLeft >=188 ){
    anglePos = 45;
  }
  else if (potValLeft >= 178){
    anglePos = 40; 
  }
  else if(potValLeft >= 168){
    anglePos = 35;
  }
  else if (potValLeft >=158 ){
    anglePos = 30; 
  }
  else if(potValLeft >=145 ){
    anglePos = 25;
  }
  else if (potValLeft >=134 ){
    anglePos = 20; 
  }
  else if(potValLeft >= 123 ){
    anglePos = 15;
  }
  else if (potValLeft >= 111 ){
    anglePos = 10; 
  }
  else if(potValLeft >= 98 ){
    anglePos = 5;
  }
  else {
    anglePos = 0; 
  }
return anglePos;
}

void open(){
  //open arm, move arm up
  
}
void close(){
  //close, move arm down
  
}
void up(){
  leftBaseServo.write(90);
  rightBaseServo.write(90);
  delay(1000);
}
void down(){
  leftBaseServo.write(0);
  rightBaseServo.write(0);
  delay(1000);
}
void nod(){
  //up down, arm nods twice
  up();
  down();
  up();
  down();
  up();
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
  leftBaseServo.write(0);
  rightBaseServo.write(0);
  turnTableServo.write(0);
  phoneMountServo.write(90);
  delay(1000); 
}
/*Emergency Shut Down*/
void emergencyShutDown(){
  //stop all motor movement
}
/*Regular open*/
void openCompletely(){
//open arm to upright pos

}
/*Normal Shut Down*/
void shutDown(){
  //need to make sure all other motors are in correct postion to close
//close arm all the way
}

/*******************************************************************/
/* put your main code here, to run repeatedly: */
void loop() { 

  if (Serial.available() > 0) {//serial is reading stuff 
    serialData = Serial.read(); 

    if(serialData == '0'){ 
      homeServos();
    }
    //phone mount serials ****************************************
    else if (serialData == '1'){
      portrait();
    }
    else if(serialData == '2'){
      landscape();
    }
    else if (serialData == '3'){ //move left ccw
      int currPos = getPositionPM();
      int newPos = currPos +5;
      if (newPos <=180){
        phoneMountServo.write(newPos);
        delay(1000);
      }//else no movement, at limit
    } 
    else if(serialData == '4'){ //move right cw
      int currPos = getPositionPM();
      int newPos = currPos - 5;
      if( newPos >= 0){
        phoneMountServo.write(newPos); 
        delay(1000); 
      }//else no movement, at limit
    }
    //base motor serials ****************************************
    else if (serialData == '5'){ //move left
      int currPos = getPositionBM();
      int newPos = currPos + 5;
      if( newPos <= 180){
        leftBaseServo.write(newPos); 
        rightBaseServo.write(newPos); 
        delay(1000);
      }//else no movement, at limit
    }
    else if(serialData == '6'){ //move right
      int currPos = getPositionBM();
      int newPos = currPos - 5;
      if( newPos >= 0){
        leftBaseServo.write(newPos);  
        rightBaseServo.write(newPos);
        delay(1000);
      }//else no movement, at limit
    }
    else if (serialData == '7'){ //move servos to 180
      leftBaseServo.write(180);
      rightBaseServo.write(180);
      delay(1000);
    }
    else if (serialData == '8'){
      nod();
    }
    //end else if serialData value
    
  } //end serial available

} //end loop
