String comdata = "";
char terminator = ';';
void setup() {
  Serial.begin(19200);
  while (Serial.read() >= 0) {} //clear serialbuffer
  Serial.println("1:DI,2:DO,3:AI,4:AO");
}
void loop() {

  //digitalWrite(int('5')-64, HIGH);
  // read data from serial port
  // if (Serial.available() > 0) {
  //  comdata = Serial.readStringUntil(terminator);
  //  delay(100);
  //    Serial.print("Serial.readStringUntil: ");
  //Serial.println(comdata);

  while (Serial.available() > 0)
  {
    comdata += char(Serial.read());
    delay(2);
  }
  if (comdata.length() > 0)
    if (comdata[0] == ':')
      switch (comdata[1]) {
        case '1':
          Serial.println('1');
          pinMode(int(comdata[2]) - '0', INPUT_PULLUP);
          Serial.print(comdata[2]);
          Serial.print(digitalRead((int)comdata[2]-'0'));
          break;
        case '2':
          Serial.print('2');
          Serial.print(comdata[2] - '0');

          pinMode((int)comdata[2] - '0', OUTPUT);
          Serial.print("_OUTPUT");
          if (comdata[3] == '1') {
            digitalWrite((int)comdata[2] - '0', HIGH);
            Serial.println("_HIGH");
          }
          if (comdata[3] == '0') {
            Serial.println("_LOW");
            digitalWrite(int(comdata[2]) - '0', LOW);
          }

          break;
        case '3':

          Serial.print('3');
          break;
        case '4':
          Serial.print('4');
          break;
        case '5':
          Serial.print('5');
          break;
      }

  while (Serial.read() >= 0) {};
  comdata = "";
}


