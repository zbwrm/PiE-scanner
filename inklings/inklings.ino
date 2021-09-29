#include <Servo.h>

int angles[2];
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
  angles[0] = recieveAngle();
  angles[1] = recieveAngle();
  
  while (Serial.available() > 0) {
    Serial.read();
  }
  // move to new angles

  vert.write(angles[0]);
  horz.write(angles[1]);

  
  currentMeasurement = takeMeasurements();

//  Serial.println("<measurement>");
  Serial.println(int(currentMeasurement));
  // println it in serial
  
  // wait? maybe?
  delay(100);
}

int recieveAngle() {
  int outAngle;
  outAngle = Serial.read();
  return outAngle;
}

int takeMeasurements() {
  int measureSum = 0;
  int measureAvg;
  for (int i = 0; i < 8; i++){
    measureSum += analogRead(A0);
    delay(25);
  }
  measureAvg = measureSum / 8;
  return measureAvg;
}
