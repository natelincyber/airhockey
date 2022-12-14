#include <Servo.h>
#include <Arduino.h>


Servo servo;

int pos = 0;

void setup() {
    servo.attach(7);
}

void loop() {
    for (pos = 0; pos <= 180; pos += 5) { // goes from 0 degrees to 180 degrees
	    // in steps of 1 degree
	    servo.write(pos);              // tell servo to go to position in variable 'pos'
	    delay(10);                       // waits 15ms for the servo to reach the position
	  }
	  for (pos = 180; pos >= 0; pos -= 5) { // goes from 180 degrees to 0 degrees
	    servo.write(pos);              // tell servo to go to position in variable 'pos'
	    delay(10);                       // waits 15ms for the servo to reach the position
	  }
}