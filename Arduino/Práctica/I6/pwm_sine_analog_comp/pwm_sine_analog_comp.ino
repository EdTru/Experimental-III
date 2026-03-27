// ============================================================
//  PWM Sine Wave Generator — Internal Analog Comparator Trigger
//
//  Uses the Arduino's built-in analog comparator (no external IC).
//  Detects zero-crossing of an external sine wave on AIN0 (pin 6),
//  referenced against 2.5V on AIN1 (pin 7) via resistor divider.
//  Starts generating the PWM sine on pin 9 only when stopped.
//  Send 'stop' via Serial Monitor to reset and wait for next trigger.
//
//  Hardware connections:
//    Pin 9   --> R (22 kΩ) --> V_out, C (47 nF) to GND  [PWM output + RC filter]
//    Pin 6   --> External sine wave input (AIN0)
//    Pin 7   --> 2.5V reference: 5V--[10kΩ]--pin7--[10kΩ]--GND  (AIN1)
//
//  NOTE: pins 6 and 7 must NOT be used as digitalWrite/analogWrite
//        while the analog comparator is active.
// ============================================================

// --- Pins ---
const int PWM_PIN = 9;   // PWM output (Timer1, OC1A)
// AIN0 = pin 6 (external sine input)
// AIN1 = pin 7 (2.5V resistor divider reference)

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
float    frequency    = 1.0;
long     stepDelay_us = 0;
int      sampleIndex  = 0;
volatile bool triggered = false;  // Set by analog comparator ISR
bool     running      = false;

void setup() {
  Serial.begin(9600);

  pinMode(PWM_PIN, OUTPUT);
  // Pins 6 and 7 are left as INPUT (default) — do not configure them

  // --- Boost Timer1 to ~62.5 kHz fast PWM on pin 9 ---
  TCCR1A = _BV(COM1A1) | _BV(WGM10);
  TCCR1B = _BV(WGM12)  | _BV(CS10);

  // --- Configure internal analog comparator ---
  ADCSRB &= ~_BV(ACME);   // Use AIN1 (pin 7) as negative input, not ADC mux
  ACSR =  (0 << ACD)    | // Comparator ON  (ACD=0 enables it)
          (0 << ACBG)   | // External pin AIN1 as reference (not internal bandgap)
          (1 << ACIE)   | // Enable analog comparator interrupt
          (1 << ACIS1)  | // ACIS1:ACIS0 = 11 → interrupt on rising edge
          (1 << ACIS0);   //

  // Output midpoint (2.5V DC) while waiting for trigger
  OCR1A = 128;

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
      OCR1A     = 128;
      Serial.println(">> Stopped. Waiting for next zero-crossing on pin 6.");
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
    sampleIndex = 0;
    Serial.println(">> Zero-crossing detected — sine started.");
  }

  // --- Output sine samples ---
  if (running) {
    OCR1A = sineTable[sampleIndex];
    sampleIndex = (sampleIndex + 1) & 0xFF;
    delayMicroseconds(stepDelay_us);
  }
}

// ---- Analog Comparator ISR — fires on rising zero-crossing ----
ISR(ANALOG_COMP_vect) {
  if (!running) {
    triggered = true;
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
  Serial.println("  PWM Sine — Analog Comparator Trigger");
  Serial.println("========================================");
  Serial.println("Connections:");
  Serial.print("  PWM output : pin "); Serial.println(PWM_PIN);
  Serial.println("  Ext. sine  : pin 6 (AIN0)");
  Serial.println("  Reference  : pin 7 (AIN1)");
  Serial.println("              5V--[10k]--pin7--[10k]--GND");
  Serial.println();
  Serial.println("RC filter on pin 9:");
  Serial.println("  R = 22 kOhm, C = 47 nF");
  Serial.println();
  Serial.println("Commands:");
  Serial.println("  <number>  Set frequency in Hz");
  Serial.println("  stop      Stop sine, wait for next trigger");
  Serial.println();
  Serial.println("Waiting for zero-crossing on pin 6...");
  Serial.println("========================================");
}
