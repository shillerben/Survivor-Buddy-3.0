/*
  AnalogReadSerial

  Reads an analog input on pin 0, prints the result to the Serial Monitor.
  Graphical representation is available using Serial Plotter (Tools > Serial Plotter menu).
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/AnalogReadSerial
*/

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  Serial.println("Waiting for USB data...");
  Serial.setTimeout(100);
}

// the loop routine runs over and over again forever:
void loop() {
  // read the data from USB
  String data;
  if (Serial.available() > 0) {
      data = Serial.readString();
      // print out the value you read:
      Serial.print(data);
  }
  
  //delay(1);        // delay in between reads for stability
}
