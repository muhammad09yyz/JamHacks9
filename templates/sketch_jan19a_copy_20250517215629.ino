const int ledPin = 9;

void setup() {
  pinMode(ledPin, OUTPUT);
  analogWrite(ledPin, 0); // Ensure LED starts OFF
  Serial.begin(9600);
  while (!Serial) { }
  Serial.println("Arduino Ready");
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "ON") {
  analogWrite(ledPin, 255); // Ensure LED starts OFF
      Serial.println("LED ON");
    } else if (command == "OFF") {
  analogWrite(ledPin, 0); // Ensure LED starts OFF
      Serial.println("LED OFF");
    } else if (command == "DIM") {
        analogWrite(ledPin, 125); // Ensure LED starts OFF

      }
      else {
      Serial.print("Unknown command: ");
      Serial.println(command);
    }
  }
}
