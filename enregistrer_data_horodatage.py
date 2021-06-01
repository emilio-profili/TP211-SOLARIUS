/**
 * Exemple de code Arduino pour un datalogger avec horodatage et stockage sur carte SD.
 */

/* Dépendances */
#include <Wire.h> // Pour la communication I2C
#include <SPI.h>  // Pour la communication SPI
#include <SD.h>   // Pour la communication avec la carte SD
#include "DS1307.h" // Pour le module DS1307


/* Rétro-compatibilité avec Arduino 1.x et antérieur */
#if ARDUINO >= 100
#define Wire_write(x) Wire.write(x)
#define Wire_read() Wire.read()
#else
#define Wire_write(x) Wire.send(x)
#define Wire_read() Wire.receive()
#endif


/** Broche CS de la carte SD */
const byte SDCARD_CS_PIN = 10; // A remplacer suivant votre shield SD

/** Nom du fichier de sortie */
const char* OUTPUT_FILENAME = "data.csv";

/** Delai entre deux prises de mesures */
const unsigned long DELAY_BETWEEN_MEASURES = 5000;


/** Fonction de conversion BCD -> decimal */
byte bcd_to_decimal(byte bcd) {
  return (bcd / 16 * 10) + (bcd % 16); 
}

/** 
 * Fonction récupérant l'heure et la date courante à partir du module RTC.
 * Place les valeurs lues dans la structure passée en argument (par pointeur).
 * N.B. Retourne 1 si le module RTC est arrêté (plus de batterie, horloge arrêtée manuellement, etc.), 0 le reste du temps.
 */
byte read_current_datetime(DateTime_t *datetime) {
  
  /* Début de la transaction I2C */
  Wire.beginTransmission(DS1307_ADDRESS);
  Wire_write((byte) 0); // Lecture mémoire à l'adresse 0x00
  Wire.endTransmission(); // Fin de la transaction I2C
 
  /* Lit 7 octets depuis la mémoire du module RTC */
  Wire.requestFrom(DS1307_ADDRESS, (byte) 7);
  byte raw_seconds = Wire_read();
  datetime->seconds = bcd_to_decimal(raw_seconds);
  datetime->minutes = bcd_to_decimal(Wire_read());
  byte raw_hours = Wire_read();
  if (raw_hours & 64) { // Format 12h
    datetime->hours = bcd_to_decimal(raw_hours & 31);
    datetime->is_pm = raw_hours & 32;
  } else { // Format 24h
    datetime->hours = bcd_to_decimal(raw_hours & 63);
    datetime->is_pm = 0;
  }
  datetime->day_of_week = bcd_to_decimal(Wire_read());
  datetime->days = bcd_to_decimal(Wire_read());
  datetime->months = bcd_to_decimal(Wire_read());
  datetime->year = bcd_to_decimal(Wire_read());
  
  /* Si le bit 7 des secondes == 1 : le module RTC est arrêté */
  return raw_seconds & 128;
}


/** Fichier de sortie avec les mesures */
File file;


/** Fonction setup() */
void setup() {
  
  /* Initialise le port I2C */
  Wire.begin();

  /* Initialisation du port série (debug) */
  Serial.begin(115200);
  
  /* Vérifie si le module RTC est initialisé */
  DateTime_t now;
  if (read_current_datetime(&now)) {
    Serial.println(F("Erreur : L'horloge du module RTC n'est pas active"));
    Serial.println(F("Configurer le module RTC avant d'utiliser ce programme"));
    for (;;); // Attend appui sur bouton RESET
  }

  /* Initialisation du port SPI */
  pinMode(10, OUTPUT); // Arduino UNO
  //pinMode(53, OUTPUT); // Arduino Mega

  /* Initialisation de la carte SD */
  Serial.println(F("Initialisation de la carte SD ... "));
  if (!SD.begin(SDCARD_CS_PIN)) {
    Serial.println(F("Erreur : Impossible d'initialiser la carte SD"));
    Serial.println(F("Verifiez la carte SD et appuyez sur le bouton RESET"));
    for (;;); // Attend appui sur bouton RESET
  }

  /* Ouvre le fichier de sortie en écriture */
  Serial.println(F("Ouverture du fichier de sortie ... "));
  file = SD.open(OUTPUT_FILENAME, FILE_WRITE);
  if (!file) {
    Serial.println(F("Erreur : Impossible d'ouvrir le fichier de sortie"));
    Serial.println(F("Verifiez la carte SD et appuyez sur le bouton RESET"));
    for (;;); // Attend appui sur bouton RESET
  }
  
  /* Ajoute l'entête CSV si le fichier est vide */
  if (file.size() == 0) {
    Serial.println(F("Ecriture de l'entete CSV ..."));
    file.println(F("Horodatage; Tension A0; Tension A1; Tension A2; Tension A3"));
    file.flush();
  }
}


/** Fonction loop() */
void loop() {
  // Temps de la précédente mesure et actuel
  static unsigned long previousMillis = 0;
  unsigned long currentMillis = millis();

  /* Réalise une prise de mesure toutes les DELAY_BETWEEN_MEASURES millisecondes */
  if (currentMillis - previousMillis >= DELAY_BETWEEN_MEASURES) {
    previousMillis = currentMillis;
    measure();
  }
}


/** Fonction de mesure - à personnaliser selon ses besoins */
void measure() {
  
  /* Lit la date et heure courante */
  DateTime_t now;
  read_current_datetime(&now);

  /* Réalise la mesure */
  float v_1 = analogRead(A0) * 5.0 / 1023; 
  float v_2 = analogRead(A1) * 5.0 / 1023;
  float v_3 = analogRead(A2) * 5.0 / 1023;
  float v_4 = analogRead(A3) * 5.0 / 1023;
  
  /* Affiche les données sur le port série pour debug */ 
  Serial.print(v_1);
  Serial.print(F("; "));
  Serial.print(v_2);
  Serial.print(F("; "));
  Serial.print(v_3);
  Serial.print(F("; "));
  Serial.println(v_4);
  
  /* Enregistre les données sur la carte SD */
  // Horodatage
  file.print(now.days);
  file.print(F("/"));
  file.print(now.months);
  file.print(F("/"));
  file.print(now.year + 2000);
  file.print(F(" "));
  file.print(now.hours);
  file.print(F(":"));
  file.print(now.minutes);
  file.print(F(":"));
  file.print(now.seconds);
  file.print(F("; "));
  // Données brutes
  file.print(v_1);
  file.print(F("; "));
  file.print(v_2);
  file.print(F("; "));
  file.print(v_3);
  file.print(F("; "));
  file.println(v_4);
  file.flush();
}
