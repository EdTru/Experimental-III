// ============================================================
//  8-bit R-2R DAC - Manual Input
//  Pins 2-9 → D0 (LSB) to D7 (MSB)
//  Enter a decimal (0-255) or binary (e.g. 10110101) via Serial Monitor
// ============================================================

// --- Pin mapping (D0=LSB to D7=MSB) ---
const int BIT_PINS[8] = {2, 3, 4, 5, 6, 7, 8, 9};

// --- Voltage reference ---
const float V_REF = 5.0;

void setup() {
  Serial.begin(9600);

  for (int i = 0; i < 8; i++) {
    pinMode(BIT_PINS[i], OUTPUT);
    digitalWrite(BIT_PINS[i], LOW);
  }

  printWelcome();
}
int value;
void loop() {
  String input = Serial.readStringUntil('\n');
  input.trim();
  Serial.print(value);
  setDAC(value);
  value = value + 1;
}

// ---- Write an 8-bit value to the DAC pins ----
void setDAC(int value) {
  for (int i = 0; i < 8; i++) {
    digitalWrite(BIT_PINS[i], (value >> i) & 0x01 ? HIGH : LOW);
  }

  float voltage = (value / 255.0) * V_REF;

  Serial.println("----------------------------------------");
  Serial.print("Decimal : ");
  Serial.println(value);
  Serial.print("Binary  : ");
  printBinary(value);
  Serial.print("Voltage : ~");
  Serial.print(voltage, 3);
  Serial.println(" V");
  Serial.print("Pins    : ");
  for (int i = 7; i >= 0; i--) {
    Serial.print("D"); Serial.print(i);
    Serial.print("="); Serial.print((value >> i) & 1);
    if (i > 0) Serial.print(" ");
  }
  Serial.println();
  Serial.println("----------------------------------------");
}

// ---- Helper: print 8-bit binary representation ----
void printBinary(int value) {
  for (int i = 7; i >= 0; i--) {
    Serial.print((value >> i) & 1);
  }
  Serial.println();
}

// ---- Helper: check if string contains only '0' and '1' (1–8 chars) ----
bool isBinaryString(String s) {
  if (s.length() < 1 || s.length() > 8) return false;
  for (unsigned int i = 0; i < s.length(); i++) {
    if (s[i] != '0' && s[i] != '1') return false;
  }
  return true;
}

// ---- Helper: check if string is a valid decimal number ----
bool isDecimalString(String s) {
  if (s.length() < 1 || s.length() > 3) return false;
  for (unsigned int i = 0; i < s.length(); i++) {
    if (!isDigit(s[i])) return false;
  }
  return true;
}

// ---- Helper: convert binary string like "10110101" to integer ----
int binaryStringToDecimal(String s) {
  int result = 0;
  for (unsigned int i = 0; i < s.length(); i++) {
    result = result * 2 + (s[i] - '0');
  }
  return result;
}

void printWelcome() {
  Serial.println("========================================");
  Serial.println("   8-bit R-2R DAC - Manual Input");
  Serial.println("========================================");
  Serial.println("Pin mapping:");
  for (int i = 0; i < 8; i++) {
    Serial.print("  D"); Serial.print(i);
    if (i == 0) Serial.print(" (LSB)");
    if (i == 7) Serial.print(" (MSB)");
    Serial.print(" -> Pin "); Serial.println(BIT_PINS[i]);
  }
  Serial.println();
  Serial.println("Input a value via Serial Monitor:");
  Serial.println("  - Decimal: 0 to 255");
  Serial.println("  - Binary:  00000000 to 11111111");
  Serial.println("Baud rate: 9600 | Line ending: Newline");
  Serial.println("========================================");
}
