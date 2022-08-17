#define IN1 9
#define IN2 8
#define IN3 7
#define IN4 6
#define speedL 10
#define speedR 5
#define Volt_sensor A0
#define cur_sensor A1
char reading;
int offset = 20;
unsigned long previousMillis = 0UL;
unsigned long interval = 300UL;
int speed_value;
void setup() {
  Serial.begin(9600);
  for (int i = 5; i <= 10; i++) {
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
void speed_Mode(){
    switch (Reading) {
      case ‘low’:
        speed_value=100; break;
      case ’mid’:
        speed_value=170; break;
      case ‘hi’:
        speed_value=255; break;
    }
  }

void loop() {
  
  
  if (Serial.available() > 0) {
    Reading = Serial.read();
    switch (Reading) {
      case ‘F’:
        forword(); break;
      case ’B’:
        backword(); break;
      case ‘R’:
        right(); break;
      case ‘L’:
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
}
