typedef union {
  float floatingPoint;
  byte binary[4];
} binaryFloat;

binaryFloat angles[2];
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
  angles = recieveAngles();
  // move to new angles

  vert.write(angles[0]);
  horz.write(angles[1]);

  
  currentMeasurement = takeMeasurements();

//  Serial.println("<measurement>");
  sendUnion(currentMeasurement);
  // println it in serial
  
  // wait? maybe?
}

void sendUnion(binaryFloat in) {
  Serial.write(in.binary,4);
  Serial.println();
}

void recieveAngles() {
  binaryFloat outAngles[2];
  Serial.println("<angles>");
  for (int i = 0; i < 8; i++) {
    if (i < 4) {
      outAngles[0].binary[i % 4] = Serial.read();
    } else {
      outAngles[1].binary[i % 4] = Serial.read();
    }
  }
  while (Serial.available > 0) {
    Serial.read();
  }
  return outAngles;
}

void takeMeasurements() {
  binaryFloat measureSum;
  for (int i = 0; i < 8; i++){
    measureSum += analogRead(A0);
    delay(10);
  }
  return (measureSum / 8);
}
