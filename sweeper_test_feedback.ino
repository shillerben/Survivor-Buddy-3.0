/*  
 *   Adapted from: https://dronebotworkshop.com
*/

// Include Arduino Servo Library


#include <Servo.h> 

// Control and feedback pins
int servoPin = 9;
int feedbackPin = A0;

// Value from feedback signal
int feedbackValue;

// Create a servo object
Servo myservo; 


void setup() 
{ 
  // Setup Serial Monitor
  Serial.begin(9600);

  
  
  // Attach myservo object to control pin
  myservo.attach(servoPin); 
  
  // Home the servo motor
  myservo.write(0);
  
  // Step through servo positions
  // Increment by 5 degrees
  for (int servoPos = 0; servoPos <=180; servoPos = servoPos + 5){
    
    // Position servo motor
    myservo.write(servoPos);
    // Allow time to get there
    delay(1000);
    
    // Read value from feedback signal
    feedbackValue = analogRead(feedbackPin);
    
    // Write value to serial monitor
    Serial.print("Position = ");
    Serial.print(servoPos);
    Serial.print("\t");
    Serial.println(feedbackValue);
  
  }

  // Move back to home position
  myservo.write(0);
  
  // Print to serial monitor when done
  Serial.println("Finished!");

}  

void loop()
{
  // Nothing in loop
}
