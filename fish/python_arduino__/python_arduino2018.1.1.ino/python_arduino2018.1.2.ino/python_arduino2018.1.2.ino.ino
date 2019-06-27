#include <EEPROM.h>

String comData = "";

void setup()
{
  Serial.begin(115200);
  for (int i = 2; i <= 13; i++)
  {
    if (EEPROM.read(i) == 0)
    {
      pinMode(i, OUTPUT);
    }
    else
    {
      pinMode(i, INPUT);
    }
    delay(25);
  }
  Serial.println("Hello! This is Arduino!");
}

void loop()
{
  while (Serial.available() > 0)
  {
    comData += char(Serial.read());
    delay(5);
  }
  if (comData.length() > 0)
  {
    //If the command is reboot, device reboot
    if (CheckCommand("reboot", comData))
    {
      Serial.println("Rebooting!");
      reboot();
    }
    //If the command is alloutput, set all pin to output
    else if (CheckCommand("show", comData) || CheckCommand("showe2p", comData))
    {
      for (int i = 2; i <= 13; i++)
      {
        if (EEPROM.read(i) == 0)
        {
          Serial.print("Pin");
          Serial.print(i);
          Serial.print("'s Mode: ");
          Serial.println("OUT");
        }
        else
        {
          Serial.print("Pin");
          Serial.print(i);
          Serial.print("'s Mode: ");
          Serial.println("IN");
        }
        delay(25);
      }
    }
    //If the command is set , set pin's state
    else if (CheckCommand("set ", comData))
    { 
      if (comData[4] != ' ' && comData[5] == ' ')
      { Serial.print("set out");
        if (comData[6] == '1')
        {
          digitalWrite((int)comData[4] - '0', HIGH);
          Serial.print("Pin-");
          Serial.print(comData[4]);
          Serial.print("'s State: ");
          Serial.println("HIGH");
        }
        if (comData[6] == '0')
        {
          digitalWrite(((int)comData[4]) - '0', LOW);
          Serial.print("Pin-");
          Serial.print(comData[4]);
          Serial.print("'s State: ");
          Serial.println("LOW");
        }
      }
      else if (comData[4] == '1' && comData[5] != ' ' && comData[6] == ' ' && ((int)comData[5] - '0') <= 3)
      {
        if (comData[7] == '1')
        {
          digitalWrite(10 + (int)comData[5] - '0', HIGH);
          Serial.print("Pin-");
          Serial.print(comData[4]);
          Serial.print(comData[5]);
          Serial.print("'s State: ");
          Serial.println("HIGH");
        }
        if (comData[7] == '0')
        {
          digitalWrite(10 + (int)comData[5] - '0', LOW);
          Serial.print("Pin-");
          Serial.print(comData[4]);
          Serial.print(comData[5]);
          Serial.print("'s State: ");
          Serial.println("LOW");
        }
      }
    }
    //If the command is alloutput, set all pin to output
    else if (CheckCommand("alloutput", comData) || CheckCommand("allout", comData))
    {
      Serial.println("Initing EEPROM, set 0/output from address 0 to 13");
      for (int i = 0; i <= 13; i++)
      {
        EEPROM.write(i, 0);
        delay(25);
      }
      Serial.println("Done,rebooting!");
      reboot();
    }
    //If the command is allinput, set all pin to input
    else if (CheckCommand("allinput", comData) || CheckCommand("allin", comData))
    {
      Serial.println("Initing EEPROM, set 1./input from address 0 to 13");
      for (int i = 0; i <= 13; i++)
      {
        EEPROM.write(i, 1);
        delay(25);
      }
      Serial.println("Done,rebooting!");
      reboot();
    }

    //If the command is read , read pin's state
    else if (CheckCommand("read ", comData))
    {
      if (comData[5] != ' ' && comData.length() == 6)
      {
        if (digitalRead(((int)comData[5] - '0')) == 1)
        {
          Serial.print("Pin-");
          Serial.print(comData[5]);
          Serial.print("'s State: ");
          Serial.println("HIGH");
        }
        if (digitalRead(((int)comData[5] - '0')) == 0)
        {
          Serial.print("Pin-");
          Serial.print(comData[5]);
          Serial.print("'s State: ");
          Serial.println("LOW");
        }
      }
      else if (comData[5] == '1' && comData.length() >= 6 && ((int)comData[6] - '0') <= 3)
      {
        if (digitalRead((10 + (int)comData[6] - '0')) == 0)
        {
          Serial.print("Pin-");
          Serial.print(comData[5]);
          Serial.print(comData[6]);
          Serial.print("'s State: ");
          Serial.println("HIGH");
        }
        if (digitalRead((10 + (int)comData[6] - '0')) == 1)
        {
          Serial.print("Pin-");
          Serial.print(comData[5]);
          Serial.print(comData[6]);
          Serial.print("'s State: ");
          Serial.println("LOW");
        }
      }

      else if ((comData[5] == 'a' || comData[5] == 'A' ) && comData.length() >= 6 && ((int)comData[6] - '0') <= 5)
      {
        Serial.print("Pin-A");
        Serial.print(comData[6]);
        Serial.print("'s Value: ");
        Serial.println(analogRead((int)comData[6] - '0'));
      }
    }

    //If the command is init, set all pin's mode , inout or output,
    //e.g.: "init 101a11100- 0" that means pin2 to pn13's mode will be "in,out,in,in,in,in,in,out,out,in,in,out"
    //char 0 will set pinmode to output, other chai will set pinmode to input
    else if (CheckCommand("init ", comData))
    {
      int comDateLength = comData.length();
      if (comDateLength >= 17)
      {
        Serial.println("Initing Pin2 to Pin13's mode.");
        for (int i = 5; i <= 16; i++)
        {
          if (comData == '0')
          {
            EEPROM.write(i - 3, 0);
            Serial.print(comData);
            Serial.print(" Pin");
            Serial.print(i - 3);
            Serial.println(" OUT");
          }
          else
          {
            EEPROM.write(i - 3, 1);
            Serial.print(comData);
            Serial.print(" Pin");
            Serial.print(i - 3);
            Serial.println(" IN");
          }
          delay(25);
        }
        Serial.println("Done,rebooting!");
        reboot();
      }
      else
      {
        Serial.println("Params error, you need to inoput 12 chars to set 12 Pins' mode!");
      }
    }
    //If the command is setall, set all pin's state high or low ,
    //e.g.: "setall 101a11100- 0" that means pin2 to pn13's mode will be "low,high,low,low,low,low,low,high,high,low,low,high"
    //char 0 will set pinmode to high, other chai will set pinmode to low
    else if (CheckCommand("setall ", comData))
    {
      int comDateLength = comData.length();
      if (comDateLength >= 19)
      {
        Serial.println("Setting up Pin2 to Pin13's State.");
        for (int i = 7; i <= 18; i++)
        {
          if (comData == '0')
          {
            digitalWrite(i - 5, HIGH);
            Serial.print(comData);
            Serial.print(" Pin");
            Serial.print(i - 5);
            Serial.println(" HIGH");
          }
          else
          {
            digitalWrite(i - 5, LOW);
            Serial.print(comData);
            Serial.print(" Pin");
            Serial.print(i - 5);
            Serial.println(" LOW");
          }
          delay(25);
        }
        Serial.println("Done!");
      }
      else
      {
        Serial.println("Params error, you need to inoput 12 chars to set 12 Pins' state!");
      }
    }
    else
    {
      Serial.println("");
      Serial.println("Command error, please try again. Below information may help you:");
      Serial.println("reboot\t\t\t\t\tReboot Arduino");
      Serial.println("showm\t\t\t\t\tShow digital pin's mode from EEPROM");
      Serial.println("init <12 pins' mode>\t\t\te.g.,init 111111111111 means set all digital pin to INPUT");
      Serial.println("allout | alloutput\t\t\tSet all digital pin to OUTPUT");
      Serial.println("allin  | allinput\t\t\tSet all digital pin to INPUT");
      Serial.println("setall <12 pins' mode>\t\t\te.g.,setall 000000000000 means set all digtal pin's status to HIGH");
      Serial.println("set <pin number> <pin status>\t\tSet digital pin's status");
      Serial.println("read <pin number> <pin status>\t\tRead pin's status or value");
      Serial.flush();
      delay(100);
      comData = "";
      return;
    }
    Serial.println(" ");
    Serial.flush();
    delay(100);
    comData = "";
  }
}

bool CheckCommand(String command, String b)
{
  int commandLength = command.length();
  for (int i = 0; i < commandLength; i++)
  {
    if (command[i] != b[i])
    {
      return false;
    }
  }
  return true;
}

void reboot()
{
  delay(100);
  void(* resetFunc) (void) = 0; //declare reset function @ address 0
  resetFunc();  //call reset
}
