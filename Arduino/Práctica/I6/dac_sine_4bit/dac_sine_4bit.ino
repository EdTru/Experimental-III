// ============================================================
//  4-bit R-2R DAC - Sine Wave Generator
//  Pins 4-7 → D0 (LSB) to D3 (MSB)
//  Type a frequency (Hz) in Serial Monitor to change it
// ============================================================

// --- Pin mapping ---
const int BIT_PINS[4] = {4, 5, 6, 7};  // D0=pin4, D1=pin5, D2=pin6, D3=pin7

// --- Sine wave config ---
const int   SAMPLES     = 32;     // Number of steps per full cycle (more = smoother)
const float V_REF       = 5.0;    // Reference voltage

// --- Precomputed 4-bit sine lookup table (0–15 range, offset to stay positive) ---
// Values = round(7.5 + 7.5 * sin(2*pi*i/SAMPLES))  for i = 0..SAMPLES-1
int sineTable[32];

// --- State ---
float   frequency    = 50.0;   // Default frequency in Hz
long    stepDelay_us = 0;     // Microseconds between samples (computed)
int     sampleIndex  = 0;
bool    running      = true;

void setup() {
  Serial.begin(9600);

  for (int i = 0; i < 4; i++) {
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
      Serial.println("ERROR: Enter a positive number in Hz (e.g. 2.5) or 'stop'.");
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
  // Period (us) / number of samples = delay per step
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
  Serial.print("Max freq  : ~");
  Serial.print(1000000.0 / (SAMPLES * 50), 1);  // ~50us min delay per step
  Serial.println(" Hz (hardware limit)");
  Serial.println("----------------------------------------");
}

// ---- Write a 4-bit value to the DAC pins ----
void setDAC(int value) {
  value = constrain(value, 0, 15);
  for (int i = 0; i < 4; i++) {
    digitalWrite(BIT_PINS[i], (value >> i) & 0x01 ? HIGH : LOW);
  }
}

// ---- Build sine lookup table scaled to 0–15 ----
void buildSineTable() {
  for (int i = 0; i < SAMPLES; i++) {
    float angle = 2.0 * PI * i / SAMPLES;
    sineTable[i] = (int)round(7.5 + 7.5 * sin(angle));
  }
}

void printWelcome() {
  Serial.println("========================================");
  Serial.println("  4-bit DAC - Sine Wave Generator");
  Serial.println("========================================");
  Serial.println("Pin mapping:");
  Serial.print("  D0 (LSB) -> Pin "); Serial.println(BIT_PINS[0]);
  Serial.print("  D1       -> Pin "); Serial.println(BIT_PINS[1]);
  Serial.print("  D2       -> Pin "); Serial.println(BIT_PINS[2]);
  Serial.print("  D3 (MSB) -> Pin "); Serial.println(BIT_PINS[3]);
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
