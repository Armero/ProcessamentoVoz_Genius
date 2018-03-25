#define LED_RED 4
#define LED_GREEN 6
#define LED_YELLOW 8
#define LED_BLUE 10

#define MAX_GAME_SIZE 10
#define SEQUENCE_DELAY 500

short int gameArray[MAX_GAME_SIZE];
short int orderLEDs[4] = {LED_RED, LED_GREEN, LED_YELLOW, LED_BLUE};
short int gameSetup = 0;
short int gameLevel = 1;

void setup() {
	pinMode(LED_RED, OUTPUT);
	pinMode(LED_GREEN, OUTPUT);
	pinMode(LED_YELLOW, OUTPUT);
	pinMode(LED_BLUE, OUTPUT);

	//digitalWrite(a, HIGH);   

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
		gameArray[i] = random(4);
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

// TERA QUE SER ALTERADA PARA O INPUT VIA SERIAL USB
void PlayerInput() {
	
	short int flagExit = 0;
	short int serialInput = -5;
	short int counterInput = -1;
	
	// DUMMY INPUT PARA TESTE
	// ORDEM DOS LEDS: C/T/C/C/C/T/C/C/C/C/C/P
	short int dummy_input[3];
	dummy_input[0] = gameArray[0];
	dummy_input[1] = gameArray[1];
	dummy_input[2] = gameArray[2]-1;
	
	while (!flagExit) {
		
		counterInput += 1;
		serialInput = dummy_input[counterInput];
	
		if (serialInput != gameArray[counterInput])
			flagExit = 1;
		else if ((serialInput == gameArray[counterInput]) && (counterInput == (gameLevel - 1)) )
			flagExit = 2;
		else if (serialInput == gameArray[counterInput]) {
			digitalWrite(orderLEDs[serialInput], HIGH);
			delay(SEQUENCE_DELAY);
			digitalWrite(orderLEDs[serialInput], LOW);
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
	digitalWrite(orderLEDs[3], HIGH);
	delay(3*SEQUENCE_DELAY);
	digitalWrite(orderLEDs[0], LOW);
	digitalWrite(orderLEDs[1], LOW);
	digitalWrite(orderLEDs[2], LOW);
	digitalWrite(orderLEDs[3], LOW);
	delay(SEQUENCE_DELAY);
	
}

void PlayerLose(){
	gameSetup = 0;
	
	for (int i = 0; i < 10; i++){
		digitalWrite(orderLEDs[0], HIGH);
		digitalWrite(orderLEDs[1], HIGH);
		digitalWrite(orderLEDs[2], HIGH);
		digitalWrite(orderLEDs[3], HIGH);
		delay(SEQUENCE_DELAY/5);
		digitalWrite(orderLEDs[0], LOW);
		digitalWrite(orderLEDs[1], LOW);
		digitalWrite(orderLEDs[2], LOW);
		digitalWrite(orderLEDs[3], LOW);
		delay(SEQUENCE_DELAY/5);
	}
	delay(SEQUENCE_DELAY);
	
}


