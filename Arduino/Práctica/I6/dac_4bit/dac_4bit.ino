// ============================================================
//  4-bit R-2R DAC Simulator
//  Pins 4-7 → D0 (LSB) to D3 (MSB)
//  Enter a decimal value (0-15) or binary string via Serial Monitor
// ============================================================

// --- Pin mapping  ---
const int BIT_PINS[4] = {4, 5, 6, 7};  // D0=pin4, D1=pin5, D2=pin6, D3=pin7

// --- Voltage reference ---
const float V_REF = 5.0;  // Reference voltage in volts

void setup() {
  Serial.begin(9600);

  // Set all bit pins as OUTPUT
  for (int i = 0; i < 4; i++) {
    pinMode(BIT_PINS[i], OUTPUT);
    digitalWrite(BIT_PINS[i], LOW);
  }

  printWelcome();
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    if (input.length() == 0) return;

    int value = -1;

    // Detect binary string (only 0s and 1s, 1–4 chars)
    if (isBinaryString(input)) {
      value = binaryStringToDecimal(input);
      Serial.print("Binary input detected: ");
      Serial.println(input);
    }
    // Detect decimal number
    else if (isDecimalString(input)) {
      value = input.toInt();
      Serial.print("Decimal input detected: ");
      Serial.println(value);
    } else {
      Serial.println("ERROR: Invalid input. Enter a decimal (0-15) or binary (e.g. 1011).");
      return;
    }

    if (value < 0 || value > 15) {
      Serial.println("ERROR: Value out of range. Must be 0-15 (or 0000-1111 in binary).");
      return;
    }

    setDAC(value);
  }
}

// ---- Write value to the 4 digital output pins ----
void setDAC(int value) {
  for (int i = 0; i < 4; i++) {
    int bitVal = (value >> i) & 0x01;  // Extract bit i
    digitalWrite(BIT_PINS[i], bitVal ? HIGH : LOW);
  }

  float voltage = (value / 15.0) * V_REF;

  Serial.println("----------------------------------------");
  Serial.print("Decimal : ");
  Serial.println(value);
  Serial.print("Binary  : ");
  printBinary(value);
  Serial.print("Voltage : ~");
  Serial.print(voltage, 3);
  Serial.println(" V");
  Serial.print("Pins    : D3=");
  Serial.print((value >> 3) & 1);
  Serial.print(" D2=");
  Serial.print((value >> 2) & 1);
  Serial.print(" D1=");
  Serial.print((value >> 1) & 1);
  Serial.print(" D0=");
  Serial.println((value >> 0) & 1);
  Serial.println("----------------------------------------");
}

// ---- Helper: print 4-bit binary representation ----
void printBinary(int value) {
  for (int i = 3; i >= 0; i--) {
    Serial.print((value >> i) & 1);
  }
  Serial.println();
}

// ---- Helper: check if string contains only '0' and '1' (1–4 chars) ----
bool isBinaryString(String s) {
  if (s.length() < 1 || s.length() > 4) return false;
  for (unsigned int i = 0; i < s.length(); i++) {
    if (s[i] != '0' && s[i] != '1') return false;
  }
  return true;
}

// ---- Helper: check if string is a valid decimal number ----
bool isDecimalString(String s) {
  if (s.length() < 1 || s.length() > 2) return false;
  for (unsigned int i = 0; i < s.length(); i++) {
    if (!isDigit(s[i])) return false;
  }
  return true;
}

// ---- Helper: convert binary string like "1011" to integer 11 ----
int binaryStringToDecimal(String s) {
  int result = 0;
  for (unsigned int i = 0; i < s.length(); i++) {
    result = result * 2 + (s[i] - '0');
  }
  return result;
}

void printWelcome() {
  Serial.println("========================================");
  Serial.println("   4-bit R-2R DAC Simulator");
  Serial.println("========================================");
  Serial.println("Pin mapping:");
  Serial.print("  D0 (LSB) -> Pin "); Serial.println(BIT_PINS[0]);
  Serial.print("  D1       -> Pin "); Serial.println(BIT_PINS[1]);
  Serial.print("  D2       -> Pin "); Serial.println(BIT_PINS[2]);
  Serial.print("  D3 (MSB) -> Pin "); Serial.println(BIT_PINS[3]);
  Serial.println();
  Serial.println("Input a value via Serial Monitor:");
  Serial.println("  - Decimal : 0 to 15");
  Serial.println("  - Binary  : 0000 to 1111");
  Serial.println("Baud rate: 9600 | Line ending: Newline");
  Serial.println("========================================");
}
