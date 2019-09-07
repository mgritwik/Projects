//int r1 = 1;
int y1 = 2;
int g1 = 3;
int r2 = 4;
int y2 = 5;
int g2 = 6;
int r3 = 7;
int y3 = 8;
int g3 = 9;
int r4 = 10;
int y4 = 11;
int g4 = 12;

int sort_desc(const void *cmp1, const void *cmp2)
{
    // Need to cast the void * to int *
    int a = *((int *)cmp1);
    int b = *((int *)cmp2);
    // The comparison
    return a > b ? -1 : (a < b ? 1 : 0);
    // A simpler, probably faster way:
    //return b - a;
}

void setup() {
    pinMode (r1, OUTPUT);
    pinMode (y1, OUTPUT);
    pinMode (g1, OUTPUT);
    
    pinMode (r2, OUTPUT);
    pinMode (y2, OUTPUT);
    pinMode (g2, OUTPUT);
    
    pinMode (r3, OUTPUT);
    pinMode (y3, OUTPUT);
    pinMode (g3, OUTPUT);
    
    pinMode (r4, OUTPUT);
    pinMode (y4, OUTPUT);
    pinMode (g4, OUTPUT);

}

void loop() {
    
    digitalWrite(g1, HIGH);
    digitalWrite(r2, HIGH);
    digitalWrite(r3, HIGH);
    digitalWrite(r4, HIGH);
    delay(9000);
    digitalWrite(g1, LOW);
    digitalWrite(r2, LOW);
    
    digitalWrite(y1, HIGH);
    digitalWrite(y2, HIGH);
    delay(3000);
    digitalWrite(y1, LOW);
    digitalWrite(y2, LOW);
    
    digitalWrite(r1, HIGH);
    digitalWrite(g2, HIGH);
    delay(9000);
    
    digitalWrite(g2, LOW);
    digitalWrite(r3, LOW);
    
    
    digitalWrite(y2, HIGH);
    digitalWrite(y3, HIGH);
    delay(3000);
    
    digitalWrite(y2, LOW);
    digitalWrite(y3, LOW);
    
    
    digitalWrite(r2, HIGH);
    digitalWrite(g3, HIGH);
    digitalWrite(r4, HIGH);
    delay(9000);
    
    digitalWrite(g3, LOW);
    digitalWrite(r4, LOW);
    
    digitalWrite(y3, HIGH);
    digitalWrite(y4, HIGH);
    delay(3000);
    
    digitalWrite(y3, LOW);
    digitalWrite(y4, LOW);
    
    digitalWrite(r3, HIGH);
    digitalWrite(g4, HIGH);
    delay(9000);
    
    digitalWrite(r3, LOW);
    digitalWrite(g4, LOW);
    digitalWrite(r1, LOW);
    digitalWrite(y1, HIGH);
    digitalWrite(y4, HIGH);
    delay(3000);
    
    digitalWrite(y1, LOW);
    digitalWrite(y4, LOW);
    
    
}

//varibles Replaced

int red1 = 1;
int yellow1 = 2;
int green1 = 3;
int red2 = 4;
int yellow2 = 5;
int green2 = 6;
int red3 = 7;
int yellow3 = 8;
int green3 = 9;
int red4 = 10;
int yellow4 = 11;
int green4 = 12;

void setup() {
    pinMode (red1, OUTPUT);
    pinMode (yellow1, OUTPUT);
    pinMode (green1, OUTPUT);
    
    pinMode (red2, OUTPUT);
    pinMode (yellow2, OUTPUT);
    pinMode (green2, OUTPUT);
    
    pinMode (red3, OUTPUT);
    pinMode (yellow3, OUTPUT);
    pinMode (green3, OUTPUT);
    
    pinMode (red4, OUTPUT);
    pinMode (yellow4, OUTPUT);
    pinMode (green4, OUTPUT);
    
 
}

void loop() {
    
    digitalWrite(green1, HIGH);
    digitalWrite(red2, HIGH);
    digitalWrite(red3, HIGH);
    digitalWrite(red4, HIGH);
    delay(4000);
    digitalWrite(green1, LOW);
    digitalWrite(red2, LOW);
    
    digitalWrite(yellow1, HIGH);
    digitalWrite(yellow2, HIGH);
    delay(1000);
    digitalWrite(yellow1, LOW);
    digitalWrite(yellow2, LOW);
    
    digitalWrite(red1, HIGH);
    digitalWrite(green2, HIGH);
    delay(4000);
    
    digitalWrite(green2, LOW);
    digitalWrite(red3, LOW);
    
    
    digitalWrite(yellow2, HIGH);
    digitalWrite(yellow3, HIGH);
    delay(1000);
    
    digitalWrite(yellow2, LOW);
    digitalWrite(yellow3, LOW);
    
    
    digitalWrite(red2, HIGH);
    digitalWrite(green3, HIGH);
    digitalWrite(red4, HIGH);
    delay(4000);
    
    digitalWrite(green3, LOW);
    digitalWrite(red4, LOW);
    
    digitalWrite(yellow3, HIGH);
    digitalWrite(yellow4, HIGH);
    delay(1000);
    
    digitalWrite(yellow3, LOW);
    digitalWrite(yellow4, LOW);
    
    digitalWrite(red3, HIGH);
    digitalWrite(green4, HIGH);
    delay(4000);
    
    digitalWrite(red3, LOW);
    digitalWrite(green4, LOW);
    digitalWrite(red1, LOW);
    digitalWrite(yellow1, HIGH);
    digitalWrite(yellow4, HIGH);
    delay(1000);
    
    digitalWrite(yellow1, LOW);
    digitalWrite(yellow4, LOW);
    
    
}

