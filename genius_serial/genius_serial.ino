#define LED_WHITE 2
#define LED_BLUE 4
#define LED_RED 6

#define MAX_GAME_SIZE 10
#define SEQUENCE_DELAY 1000

short int gameArray[MAX_GAME_SIZE];

short int orderLEDs[3] = {LED_WHITE, LED_BLUE, LED_RED};
short int gameSetup = 0;
short int gameLevel = 1;

void setup() {
	pinMode(LED_WHITE, OUTPUT);
	pinMode(LED_BLUE, OUTPUT);
	pinMode(LED_RED, OUTPUT);
	
	randomSeed(analogRead(0));
	Serial.begin(9600);
	delay(500);

}

void loop() {

	if (gameSetup == 0)
		NewGame();
	else if (gameSetup == 1)
		ShowSequence();
	else if (gameSetup == 2)
		PlayerInput();
	else if (gameSetup == 3)
		PlayerWin();
	else if (gameSetup == 4)
		PlayerLose();
		
}

void NewGame() {
	for (int i = 0; i < MAX_GAME_SIZE; i++) 
		gameArray[i] = random(3);
	
	gameSetup = 1;
	gameLevel = 1;
}

void ShowSequence() {
	for (int i = 0; i < gameLevel; i++) {
		digitalWrite(orderLEDs[gameArray[i]], HIGH);
		delay(SEQUENCE_DELAY);
		digitalWrite(orderLEDs[gameArray[i]], LOW);
	}
	gameSetup = 2;
}

void PlayerInput() {
	
	short int flagExit = 0;
	short int serialInput = -5;
	short int counterInput = -1;
	
	while (!flagExit) {

		while(Serial.available() > 0) {
			counterInput += 1;
			char inChar = (char)Serial.read();
			Serial.flush();
			
			if ( inChar == 'w')
				serialInput = 0;
			if ( inChar == 'b')
				serialInput = 1;
			if ( inChar == 'r')
				serialInput = 2;
		}

		if (serialInput == -5)
			continue;
		else if (serialInput != gameArray[counterInput]) {
			flagExit = 1;
			serialInput = -5;
		}
		else if ((serialInput == gameArray[counterInput]) && (counterInput == (gameLevel - 1)) ) {
			flagExit = 2;
			serialInput = -5;
		}
		else if (serialInput == gameArray[counterInput]) {
			digitalWrite(orderLEDs[serialInput], HIGH);
			delay(SEQUENCE_DELAY);
			digitalWrite(orderLEDs[serialInput], LOW);
			serialInput = -5;
		}
	}
	
	if (flagExit == 1)
		gameSetup = 4;
	if (flagExit == 2)
		gameSetup = 3;
}

void PlayerWin() {
	gameLevel += 1;
	
	if (gameLevel > MAX_GAME_SIZE)
		gameSetup = 0;
	else
		gameSetup = 1;
	
	digitalWrite(orderLEDs[0], HIGH);
	digitalWrite(orderLEDs[1], HIGH);
	digitalWrite(orderLEDs[2], HIGH);
	delay(3*SEQUENCE_DELAY);
	digitalWrite(orderLEDs[0], LOW);
	digitalWrite(orderLEDs[1], LOW);
	digitalWrite(orderLEDs[2], LOW);
	delay(SEQUENCE_DELAY);
	
}

void PlayerLose(){
	gameSetup = 0;
	
	for (int i = 0; i < 10; i++){
		digitalWrite(orderLEDs[0], HIGH);
		digitalWrite(orderLEDs[1], HIGH);
		digitalWrite(orderLEDs[2], HIGH);
		delay(SEQUENCE_DELAY/5);
		digitalWrite(orderLEDs[0], LOW);
		digitalWrite(orderLEDs[1], LOW);
		digitalWrite(orderLEDs[2], LOW);
		delay(SEQUENCE_DELAY/5);
	}
	delay(SEQUENCE_DELAY);
	
}


