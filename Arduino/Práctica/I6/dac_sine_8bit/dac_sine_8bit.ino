// ============================================================
//  8-bit R-2R DAC - Sine Wave Generator
//  Pins 2-9 → D0 (LSB) to D7 (MSB)
//  Type a frequency (Hz) in Serial Monitor to change it
// ============================================================

// --- Pin mapping (D0=LSB to D7=MSB) ---
const int BIT_PINS[8] = {2, 3, 4, 5, 6, 7, 8, 9};

// --- Sine wave config ---
const int   SAMPLES     = 64;    // Steps per full cycle (more = smoother)
const float V_REF       = 5.0;   // Reference voltage

// --- Precomputed 8-bit sine lookup table (0–255 range) ---
// Values = round(127.5 + 127.5 * sin(2*pi*i/SAMPLES))
int sineTable[64];

// --- State ---
float frequency    = 1.0;
long  stepDelay_us = 0;
int   sampleIndex  = 0;
bool  running      = true;

void setup() {
  Serial.begin(9600);

  for (int i = 0; i < 8; i++) {
    pinMode(BIT_PINS[i], OUTPUT);
    digitalWrite(BIT_PINS[i], LOW);
  }

  buildSineTable();
  setFrequency(frequency);
  printWelcome();
}

void loop() {
  // --- Check for new frequency input ---
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    if (input.equalsIgnoreCase("stop")) {
      running = false;
      setDAC(0);
      Serial.println(">> Signal stopped. Type a frequency (Hz) to restart.");
      return;
    }

    float newFreq = input.toFloat();
    if (newFreq > 0) {
      setFrequency(newFreq);
    } else {
      Serial.println("ERROR: Enter a positive number in Hz (e.g. 10) or 'stop'.");
    }
  }

  // --- Output next sine sample ---
  if (running) {
    setDAC(sineTable[sampleIndex]);
    sampleIndex = (sampleIndex + 1) % SAMPLES;
    delayMicroseconds(stepDelay_us);
  }
}

// ---- Set frequency and recompute step delay ----
void setFrequency(float freq) {
  frequency    = freq;
  stepDelay_us = (long)((1000000.0 / freq) / SAMPLES);
  running      = true;
  sampleIndex  = 0;

  Serial.println("----------------------------------------");
  Serial.print("Frequency : ");
  Serial.print(frequency, 2);
  Serial.println(" Hz");
  Serial.print("Step delay: ");
  Serial.print(stepDelay_us);
  Serial.println(" us");
  Serial.println("----------------------------------------");
}

// ---- Write an 8-bit value to the DAC pins ----
void setDAC(int value) {
  value = constrain(value, 0, 255);
  for (int i = 0; i < 8; i++) {
    digitalWrite(BIT_PINS[i], (value >> i) & 0x01 ? HIGH : LOW);
  }
}

// ---- Build sine lookup table scaled to 0–255 ----
void buildSineTable() {
  for (int i = 0; i < SAMPLES; i++) {
    float angle = 2.0 * PI * i / SAMPLES;
    sineTable[i] = (int)round(127.5 + 127.5 * sin(angle));
  }
}

void printWelcome() {
  Serial.println("========================================");
  Serial.println("  8-bit DAC - Sine Wave Generator");
  Serial.println("========================================");
  Serial.println("Pin mapping:");
  for (int i = 0; i < 8; i++) {
    Serial.print("  D"); Serial.print(i);
    if (i == 0) Serial.print(" (LSB)");
    if (i == 7) Serial.print(" (MSB)");
    Serial.print(" -> Pin "); Serial.println(BIT_PINS[i]);
  }
  Serial.println();
  Serial.println("Commands (Serial Monitor, 9600 baud):");
  Serial.println("  <number>  Set frequency in Hz  (e.g. 10)");
  Serial.println("  stop      Stop the signal");
  Serial.println();
  Serial.print("Running at default frequency: ");
  Serial.print(frequency);
  Serial.println(" Hz");
  Serial.println("========================================");
}
