// ============================================================
//  8-bit R-2R DAC Sine Wave Generator — TTL Zero-Crossing Trigger
//
//  Waits for a rising edge on pin 2 (TTL signal from external hardware).
//  On trigger, starts generating a sine wave via the R-2R DAC.
//  Stays running until 'stop' is sent via Serial Monitor.
//  Send any frequency (Hz) via Serial Monitor to change it.
//
//  R-2R Ladder connections (D0=LSB to D7=MSB):
//    D0 (LSB) → Pin 3
//    D1       → Pin 4
//    D2       → Pin 5
//    D3       → Pin 6
//    D4       → Pin 7
//    D5       → Pin 8
//    D6       → Pin 9
//    D7 (MSB) → Pin 10
//
//  TTL trigger:
//    External TTL signal → Pin 2 (INT0, hardware interrupt)
//    Optional: 10 kΩ pull-down resistor from pin 2 to GND
//
//  R-2R ladder: R = 10 kΩ, 2R = 20 kΩ (1% tolerance recommended)
//  V_out tapped from the MSB side of the ladder (see circuit diagram)
// ============================================================

// --- Pin mapping: D0 (LSB) to D7 (MSB) ---
const int BIT_PINS[8] = {3, 4, 5, 6, 7, 8, 9, 10};

// --- Trigger pin ---
const int TRIGGER_PIN = 2;   // INT0 — hardware interrupt

// --- Sine table: 256 samples, 8-bit (0–255) ---
const uint8_t sineTable[256] = {
  128,131,134,137,140,143,146,149,152,155,158,162,165,168,171,174,
  176,179,182,185,188,191,193,196,199,201,204,206,209,211,213,216,
  218,220,222,224,226,228,230,232,234,235,237,238,240,241,243,244,
  245,246,248,249,250,250,251,252,253,253,254,254,254,255,255,255,
  255,255,255,255,254,254,254,253,253,252,251,250,250,249,248,246,
  245,244,243,241,240,238,237,235,234,232,230,228,226,224,222,220,
  218,216,213,211,209,206,204,201,199,196,193,191,188,185,182,179,
  176,174,171,168,165,162,158,155,152,149,146,143,140,137,134,131,
  128,124,121,118,115,112,109,106,103,100, 97, 93, 90, 87, 84, 81,
   79, 76, 73, 70, 67, 64, 62, 59, 56, 54, 51, 49, 46, 44, 42, 39,
   37, 35, 33, 31, 29, 27, 25, 23, 21, 20, 18, 17, 15, 14, 12, 11,
   10,  9,  7,  6,  5,  5,  4,  3,  2,  2,  1,  1,  1,  0,  0,  0,
    0,  0,  0,  0,  1,  1,  1,  2,  2,  3,  4,  5,  5,  6,  7,  9,
   10, 11, 12, 14, 15, 17, 18, 20, 21, 23, 25, 27, 29, 31, 33, 35,
   37, 39, 42, 44, 46, 49, 51, 54, 56, 59, 62, 64, 67, 70, 73, 76,
   79, 81, 84, 87, 90, 93, 97,100,103,106,109,112,115,118,121,124
};

// --- State ---
float         frequency    = 1.0;
long          stepDelay_us = 0;
int           sampleIndex  = 0;
volatile bool triggered    = false;  // Set by ISR on rising TTL edge
bool          running      = false;

void setup() {
  Serial.begin(9600);

  // Set all R-2R pins as output, start at 0 (0V)
  for (int i = 0; i < 8; i++) {
    pinMode(BIT_PINS[i], OUTPUT);
    digitalWrite(BIT_PINS[i], LOW);
  }

  // Trigger pin as input
  pinMode(TRIGGER_PIN, INPUT);

  // Hardware interrupt on pin 2, rising edge
  attachInterrupt(digitalPinToInterrupt(TRIGGER_PIN), onTTLTrigger, RISING);

  setFrequency(frequency);
  printWelcome();
}

void loop() {
  // --- Handle Serial commands ---
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    if (input.equalsIgnoreCase("stop")) {
      running   = false;
      triggered = false;
      setDAC(128);  // Output midpoint (~2.5V) while idle
      Serial.println(">> Stopped. Waiting for next TTL trigger on pin 2.");
      return;
    }

    float newFreq = input.toFloat();
    if (newFreq > 0) {
      setFrequency(newFreq);
    } else {
      Serial.println("ERROR: Enter a positive number in Hz (e.g. 2) or 'stop'.");
    }
  }

  // --- Start sine on trigger if not already running ---
  if (triggered && !running) {
    triggered   = false;
    running     = true;
    sampleIndex = 0;    // Always start from zero-crossing point of the sine
    Serial.println(">> TTL trigger detected — sine started.");
  }

  // --- Output sine samples via R-2R DAC ---
  if (running) {
    setDAC(sineTable[sampleIndex]);
    sampleIndex = (sampleIndex + 1) & 0xFF;  // Wrap at 256
    delayMicroseconds(stepDelay_us);
  }
}

// ---- ISR: fires instantly on rising edge of TTL signal on pin 2 ----
void onTTLTrigger() {
  if (!running) {
    triggered = true;
  }
}

// ---- Write 8-bit value to R-2R DAC pins ----
void setDAC(int value) {
  value = constrain(value, 0, 255);
  for (int i = 0; i < 8; i++) {
    digitalWrite(BIT_PINS[i], (value >> i) & 0x01 ? HIGH : LOW);
  }
}

// ---- Set frequency and recompute step delay ----
void setFrequency(float freq) {
  frequency    = freq;
  stepDelay_us = (long)((1000000.0 / freq) / 256.0);

  Serial.println("----------------------------------------");
  Serial.print("Frequency : ");
  Serial.print(frequency, 3);
  Serial.println(" Hz");
  Serial.print("Step delay: ");
  Serial.print(stepDelay_us);
  Serial.println(" us");
  Serial.println("----------------------------------------");
}

void printWelcome() {
  Serial.println("========================================");
  Serial.println("  R-2R DAC Sine — TTL Trigger Sync");
  Serial.println("========================================");
  Serial.println("R-2R pin mapping:");
  for (int i = 0; i < 8; i++) {
    Serial.print("  D"); Serial.print(i);
    if (i == 0) Serial.print(" (LSB)");
    if (i == 7) Serial.print(" (MSB)");
    Serial.print(" -> Pin "); Serial.println(BIT_PINS[i]);
  }
  Serial.println();
  Serial.print("TTL trigger : pin "); Serial.println(TRIGGER_PIN);
  Serial.println("  Rising edge starts the sine.");
  Serial.println("  Optional: 10 kΩ pull-down from pin 2 to GND.");
  Serial.println();
  Serial.println("Commands:");
  Serial.println("  <number>  Set frequency in Hz");
  Serial.println("  stop      Stop sine, wait for next trigger");
  Serial.println();
  Serial.println("Waiting for TTL trigger on pin 2...");
  Serial.println("========================================");
}
