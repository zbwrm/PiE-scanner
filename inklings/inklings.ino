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
  angles[0] = recieveAngle();
  angles[1] = recieveAngle();

  // clear serial (just in case)
  while (Serial.available() > 0) {
    Serial.read();
  }

  
  // move to new angles
  if (angles[0] != oldAngles[0]) {
    horz.write(angles[0]);
    delay(100);
  }
  vert.write(angles[1]);
  delay(75);
  
  
  
  currentMeasurement = takeMeasurements();

//  Serial.println("<measurement>");
  Serial.println(int(currentMeasurement));
  // println it in serial
  
  // wait? maybe?
}

int recieveAngle() {
  int outAngle;
  outAngle = Serial.read();
  return outAngle;
}

//int takeMeasurements() {
//  int measureSum = 0;
//  int measureAvg;
//  for (int i = 0; i < 3; i++){
//    measureSum += analogRead(A0);
//    delay(25);
//  }
//  measureAvg = measureSum / 3;
//  return measureAvg;
//}

int takeMeasurements() {
  return analogRead(A0);
}
