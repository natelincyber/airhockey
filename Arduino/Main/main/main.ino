#include <LiquidCrystal.h>
#include <Servo.h>

#define btnRIGHT 0
#define btnUP 1
#define btnDOWN 2
#define btnLEFT 3
#define btnSELECT 4
#define btnNONE 5

byte checkMark[8] = {
  0b00000,
  0b00000,
  0b00001,
  0b00010,
  0b10100,
  0b01000,
  0b00000,
  0b00000
};

int adc_key_in = 0;
String data = "";
int x = 0;
int y = 0;

int midpoint = 640;

//true if playing against robot
boolean botOn = false;

LiquidCrystal lcd(8, 9, 4, 5, 6, 7);
Servo servo;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);

  servo.attach(11);

  
  lcd.begin(16,2);
  lcd.createChar(0,checkMark);
  lcd.setCursor(3,0);
  lcd.print("Air Hockey");
  delay(3000);
  lcd.clear();

  lcd.setCursor(1,0);
  lcd.print("Calibrating...");
  servo.write(0);
  delay(750);
  servo.write(180);
  delay(750);
  servo.write(90);
  delay(3000);
  lcd.clear();

  
  
  lcd.setCursor(0,0);
  while(true) {
    lcd.setCursor(0,0);
    lcd.print("Robot");
    lcd.setCursor(0,1);
    lcd.print("Human");

    if (readButtons() == btnUP) {
      lcd.setCursor(9,1);
      lcd.print("   ");
      lcd.setCursor(9,0);
      lcd.write((byte)0);
      botOn = true;
    } else if(readButtons() == btnDOWN) {
      lcd.setCursor(9,0);
      lcd.print("   ");
      lcd.setCursor(9,1);
      lcd.write((byte)0);
      botOn = false;
    }
    
    if (readButtons() == btnSELECT) {
        lcd.clear();
        Serial.print("ready");
        break;
    }
  }
  
}

int readButtons() {
   adc_key_in = analogRead(0);
 
 if (adc_key_in > 1000) return btnNONE;

 if (adc_key_in < 50) return btnRIGHT;
 if (adc_key_in < 250) return btnUP;
 if (adc_key_in < 450) return btnDOWN;
 if (adc_key_in < 650) return btnLEFT;
 if (adc_key_in < 850) return btnSELECT;
}

void loop() {
  //  lcd.setCursor(0,0);
  //  String mode = (botOn ? "Robot" : "Human");
  //
  //  lcd.print(mode);
  
    if(botOn) {
      if(!Serial.available()) {
          lcd.setCursor(3,0);
          lcd.print("waiting...");
      } else {
          lcd.setCursor(0,0);
          lcd.print("                  ");
          data = Serial.readString();
          
          for(int i = 0; i < data.length(); i++ ) {
            char c = data[i];
            if(c == '|') {
              x = data.substring(0, i).toInt();
              y = data.substring(i+1).toInt();
      
            }
          } 
  
          
          servo.write(90);
          if (x > midpoint + 5) {
            int dist = (x - midpoint)/5;
  
            servo.write(90 - dist);
          
          }

          if (x < midpoint - 5) {
            int dist = (midpoint - x)/5;
  
            servo.write(90 + dist);
 
          
          }
          
        lcd.setCursor(1,1);
        lcd.print(x);
        lcd.setCursor(5,1);
        lcd.print(y);
        
    }
  } else {}
 

  
}
