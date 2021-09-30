#include <Servo.h>

int angles[2];
int oldAngles[2];
float currentMeasurement;


Servo vert;
Servo horz;

void setup() {
  // put your setup code here, to run once:


  Serial.begin(9600);
  Serial.println("<open>");
  vert.attach(8);
  horz.attach(7);

}

void loop() {

  // recieve/unpack new angles
  Serial.println("<angles>");
  oldAngles[0] = angles[0];
  oldAngles[1] = angles[1];
  angles[0] = receive_angle();
  angles[1] = receive_angle();

  // clear serial (just in case)
  while (Serial.available() > 0) {
    Serial.read();
  }

  
  // move to new angles
  if (angles[0] != oldAngles[0]) {
    horz.write(angles[0]);
    delay(150);
  }
  vert.write(angles[1]);
  delay(75);
  
  
  
  currentMeasurement = take_measurements();

//  Serial.println("<measurement>");
  Serial.println(int(currentMeasurement));
  // println it in serial
  
  // wait? maybe?
}

int receive_angle() {
  int outAngle;
  outAngle = Serial.read();
  return outAngle;
}

int take_measurements() {
 int lowestMeasurement;
 int newMeasurements;

 for (int i = 0; i < 3; i++){
   newMeasurements = analogRead(A0);
   if (newMeasurements < lowestMeasurement){
     lowestMeasurement = newMeasurements;
   }
   delay(25);
 }
 return lowestMeasurement;
}