#pragma config(Motor,  port2,           arm_lu,        tmotorVex393_MC29, openLoop)
#pragma config(Motor,  port3,           arm_ld,        tmotorVex393_MC29, openLoop)
#pragma config(Motor,  port4,           base_br,       tmotorVex393HighSpeed_MC29, openLoop, reversed)
#pragma config(Motor,  port5,           grab_l,        tmotorVex393_MC29, openLoop)
#pragma config(Motor,  port6,           grab_r,        tmotorVex393_MC29, openLoop, reversed)
#pragma config(Motor,  port7,           base_bl,       tmotorVex393HighSpeed_MC29, openLoop)
#pragma config(Motor,  port8,           arm_ru,        tmotorVex393_MC29, openLoop)
#pragma config(Motor,  port9,           arm_rd,        tmotorVex393_MC29, openLoop, reversed)
//*!!Code automatically generated by 'ROBOTC' configuration wizard               !!*//

//base_fl		-> front right base
//base_fr		-> front left base
//base_bl		-> back left base
//base_br		-> back right base
//arm_lu		-> left side upper arm motor
//arm_ld		-> left side lower arm motor
//arm_ru		-> right side arm upper motor
//arm_rd		-> right side arm lower motor
//grab_l		-> left grab
//grab_r		-> right grab

int config_base_sensitivity = 1;
int config_arm_speed = 100;
int config_arm_hover_speed = 0;
int config_claw_speed = 60;

//CONTROL CONFIGURATION
int control_left_input() {
	return vexRT[Ch3];
}
int control_right_input() {
	return vexRT[Ch2];
}
bool control_arm_up() {
	return (bool)vexRT[Btn6U];
}
bool control_arm_down() {
	return (bool)vexRT[Btn6D];
}
bool control_claw_close() {
	return (bool)vexRT[Btn5D];
}
bool control_claw_open() {
	return (bool)vexRT[Btn5U];
}

//MOVE FUNCTIONS
void base_move(int left, int right) {
	motor(base_bl) = left;
//	motor(base_fl) = left;
	motor(base_br) = right;
//	motor(base_fr) = right;
}

void arm_move(int speed) {
	motor(arm_lu) = speed;
	motor(arm_ld) = speed;
	motor(arm_ru) = speed;
	motor(arm_rd) = speed;
}

void claw_move(int speed) {
	motor(grab_l) = speed;
	motor(grab_r) = speed;
}

//DO FUNCTIONS
void do_base() {
	int left = control_left_input() * config_base_sensitivity;
	int right = control_right_input() * config_base_sensitivity;
	base_move(left, right);
}

void do_arm() {
	if (control_arm_up()) {
		arm_move(config_arm_speed);
	} else if (control_arm_down()) {
		arm_move(-config_arm_speed);
	} else {
		arm_move(config_arm_hover_speed);
	}
}

void do_claw() {
	if (control_claw_open()) {
		claw_move(config_claw_speed);
	} else if (control_claw_close()) {
		claw_move(-config_claw_speed);
	} else {
		claw_move(0);
	}
}

//MAIN TASK
task main() {
	while (true) {
		do_base();
		do_arm();
		do_claw();
	}
}