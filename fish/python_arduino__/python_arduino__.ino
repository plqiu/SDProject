String comdata = "";
char terminator = ';';
void setup() {
  Serial.begin(19200);
  while (Serial.read() >= 0) {} //clear serialbuffer
  Serial.println("1:DO,2:DI,3:AI,4:AO");
}
void loop() {
  // read data from serial port
  if (Serial.available() > 0) {
    // delay(100);
    comdata = Serial.readStringUntil(terminator);
    //    Serial.print("Serial.readStringUntil: ");
    //Serial.println(comdata);
    if (comdata[0] == ':')
      switch (comdata[1]) {
        case '1':
          Serial.println('1');
          break;
        case '2':
          Serial.println('2');
          break;
        case '3':
          Serial.println('3');
          break;
        case '4':
          Serial.println('4');
          break;
        case '5':
          Serial.println('5');
          break;
      }
    switch (comdata[2]) {
      case '1':
        Serial.println('1');
        break;
      case '2':
        Serial.println('2');
        break;
      case '3':
        Serial.println('3');
        break;
      case '4':
        Serial.println('4');
        break;
      case '5':
        Serial.println('5');
        break;
    }
  }
  while (Serial.read() >= 0) {}
}

