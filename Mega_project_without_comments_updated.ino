#include <Servo.h>
Servo ESC1;     // create servo object to control the ESC1
Servo ESC2;     // create servo object to control the ESC2
#define Mode 1  //motors mode(1 for DC and 0 for ESC)

#define IN1 12
#define IN2 8
#define IN3 7
#define IN4 4
#define speedL 6
#define speedR 11

#define Volt_sensor A0
#define cur_sensor A1

#define ledR 3
#define ledG 5
#define ledB 2

char Reading;
int offset = 20;
unsigned long previousMillis = 0UL;
unsigned long interval = 300UL;
int speed_value;
void setup() {
  if(Mode==0){
  ESC1.attach(9, 1000, 2000);
  ESC2.attach(10, 1000, 2000);
  }Serial.begin(9600);
  for (int i = 2; i <= 12; i++) {
    pinMode(i , OUTPUT );
  }
}
void forward() {
  speed_Mode();
  digitalWrite(IN1 , HIGH);
  digitalWrite(IN2 , LOW );
  digitalWrite(IN3 , HIGH );
  digitalWrite(IN4 , LOW);
  analogWrite(speedL, speed_value);
  analogWrite(speedR, speed_value);
}
void backward() {
  speed_Mode();
  digitalWrite(IN1 , LOW);
  digitalWrite(IN2 , HIGH );
  digitalWrite(IN3 , LOW );
  digitalWrite(IN4 , HIGH);
  analogWrite(speedL, speed_value);
  analogWrite(speedR, speed_value);
}
void left() {
  speed_Mode();
  digitalWrite(IN1 , LOW);
  digitalWrite(IN2 , LOW );
  digitalWrite(IN3 , HIGH );
  digitalWrite(IN4 , LOW);
  analogWrite(speedL, speed_value);
  analogWrite(speedR, speed_value);
}
void right() {
  speed_Mode();
  digitalWrite(IN1 , HIGH);
  digitalWrite(IN2 , LOW );
  digitalWrite(IN3 , LOW );
  digitalWrite(IN4 , LOW);
  analogWrite(speedL, speed_value);
  analogWrite(speedR, speed_value);
}
void stopp() {
  speed_Mode();
  digitalWrite(IN1 , LOW);
  digitalWrite(IN2 , LOW );
  digitalWrite(IN3 , LOW );
  digitalWrite(IN4 , LOW);
  analogWrite(speedL, 0);
  analogWrite(speedR, 0);
}
void speed_Mode() {
  switch (Reading) {
    case 'low':
      analogWrite(ledR, 0);
      analogWrite(ledG, 255);
      digitalWrite(ledB, 0);
      speed_value = 100; break;
    case 'mid':
      analogWrite(ledR, 255);
      analogWrite(ledG, 255);
      digitalWrite(ledB, 0);
      speed_value = 170; break;
    case 'hi':
      analogWrite(ledR, 255);
      analogWrite(ledG, 0);
      digitalWrite(ledB, 0);
      speed_value = 255; break;
    default:
      speed_value = 120;
  }
}
void brushless() {
  speed_Mode();
  speed_value = map(speed_value, 0, 255, 1000, 2000);   // scale it to use it with the servo library (value between 0 and 180)
  ESC1.write(speed_value);    // Send the signal to ESC1
  ESC2.write(speed_value);    // Send the signal to ESC2
}

void loop() {

  if (Mode == 1) {
    if (Serial.available() > 0) {
      Reading = Serial.read();
      switch (Reading) {
        case 'F':
          forward(); break;
        case 'B':
          backward(); break;
        case 'R':
          right(); break;
        case 'L':
          left(); break;
        default:
          stopp();
      }
    }
    unsigned long currentMillis = millis();
    if (currentMillis - previousMillis > interval)
    {
      //voltage sensor reading and output
      double voltage = map(analogRead(Volt_sensor), 0, 1023, 0, 2500) + offset;
      voltage /= 100;
      Serial.print("Voltage: ");
      Serial.print(voltage);
      Serial.println("V");
      //Current sensor reading and output
      float volt_cur = analogRead(cur_sensor) * 5 / 1023.0;
      float current = (volt_cur - 2.5) / 0.185;
      if (current < 0.16) {
        current = 0;
      }
      Serial.print("Current : ");
      Serial.println(current);

      previousMillis = currentMillis;
    }
  } else if (Mode == 0) {
    unsigned long currentMillis = millis();
    if (currentMillis - previousMillis > interval)
    {
      brushless();
      previousMillis = currentMillis;
    }
  }
}
