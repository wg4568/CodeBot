/* Code auto generated from C:\Users\Branham Robotics\Documents\Code\test.cb - CodeBot language by William Gardner */
#pragma config(Motor,port2,MOTOR_arm_right_upper,tmotorVex393_MC29,openLoop,reversed)
#pragma config(Motor,port3,MOTOR_arm_right_lower,tmotorVex393_MC29,openLoop,reversed)
#pragma config(Motor,port4,MOTOR_arm_left_upper,tmotorVex393_MC29,openLoop)
#pragma config(Motor,port5,MOTOR_arm_left_lower,tmotorVex393_MC29,openLoop)
#pragma config(Motor,port6,MOTOR_base_front_left,tmotorVex393_MC29,openLoop)
#pragma config(Motor,port7,MOTOR_base_back_left,tmotorVex393_MC29,openLoop)
#pragma config(Motor,port8,MOTOR_base_right_all,tmotorVex393_MC29,openLoop)
#pragma config(Motor,port9,MOTOR_latch_motor,tmotorVex393_MC29,openLoop,reversed)
#pragma platform(VEX2)
#pragma competitionControl(Competition)
#include "Vex_Competition_Includes.c"
void pre_auton() {
	/* preauton */
}
void GROUP_latch(float s) {
	motor(MOTOR_latch_motor) = s;
}
void GROUP_base_left(float s) {
	motor(MOTOR_base_front_left) = s;
	motor(MOTOR_base_back_left) = s;
}
void GROUP_base_right(float s) {
	motor(MOTOR_base_right_all) = s;
}
void GROUP_arm_unit(float s) {
	motor(MOTOR_arm_right_upper) = s;
	motor(MOTOR_arm_right_lower) = s;
	motor(MOTOR_arm_left_upper) = s;
	motor(MOTOR_arm_left_lower) = s;
}
task autonomous() {
	GROUP_latch(25.0);
	wait1Msec(500.0);
	GROUP_latch(0.0);
	GROUP_base_left(100.0);
	GROUP_base_right(100.0);
	wait1Msec(1000.0);
	GROUP_base_left(0.0);
	GROUP_base_right(0.0);
	GROUP_arm_unit(100.0);
	wait1Msec(500.0);
	GROUP_arm_unit(0.0);
	GROUP_base_left(-100.0);
	GROUP_base_right(-100.0);
	wait1Msec(1000.0);
	GROUP_base_left(0.0);
	GROUP_base_right(0.0);
}
task usercontrol() {
		while (true) {
		BIND_arm_unit();
		BIND_latch();
		BIND_base_left();
		BIND_base_right();
	}
}

/* ===== BUILD LOG =====

[loaded file] C:\Users\Branham Robotics\Documents\Code\test.cb - 973 bytes
[extracted arguments] {'logcomment': True, 'tidy': True, 'competition': True, 'custom': False}
[removed comments] []
[parsed command] ['define', 'motor', 'arm_right_upper'] ['port 2', 'reversed']
[parsed command] ['define', 'motor', 'arm_right_lower'] ['port 3', 'reversed']
[parsed command] ['define', 'motor', 'arm_left_upper'] ['port 4']
[parsed command] ['define', 'motor', 'arm_left_lower'] ['port 5']
[parsed command] ['define', 'motor', 'base_front_left'] ['port 6']
[parsed command] ['define', 'motor', 'base_back_left'] ['port 7']
[parsed command] ['define', 'motor', 'base_right_all'] ['port 8']
[parsed command] ['define', 'motor', 'latch_motor'] ['port 9', 'reversed']
[parsed command] ['group', 'motor', 'latch'] ['latch_motor']
[parsed command] ['group', 'motor', 'base_left'] ['base_front_left', 'base_back_left']
[parsed command] ['group', 'motor', 'base_right'] ['base_right_all']
[parsed command] ['group', 'motor', 'arm_unit'] ['arm_right_upper', 'arm_right_lower', 'arm_left_upper', 'arm_left_lower']
[parsed command] ['bind', 'group', 'arm_unit', 'button'] ['input 6U 100', 'input 6D -50', 'rest 20']
[parsed command] ['bind', 'group', 'latch', 'button'] ['input 8D -25', 'input 8R 25']
[parsed command] ['bind', 'group', 'base_left', 'channel'] ['input 3']
[parsed command] ['bind', 'group', 'base_right', 'channel'] ['input 2']
[parsed command] ['auton'] ['run latch 25 500', 'run base_left base_right 100 1000', 'run arm_unit 100 500', 'run base_left base_right -100 1000']
[built command] #pragma config(Motor,port2,MOTOR_arm_right_upper,tmotorVex393_MC29,openLoop,reversed)
[built command] #pragma config(Motor,port3,MOTOR_arm_right_lower,tmotorVex393_MC29,openLoop,reversed)
[built command] #pragma config(Motor,port4,MOTOR_arm_left_upper,tmotorVex393_MC29,openLoop)
[built command] #pragma config(Motor,port5,MOTOR_arm_left_lower,tmotorVex393_MC29,openLoop)
[built command] #pragma config(Motor,port6,MOTOR_base_front_left,tmotorVex393_MC29,openLoop)
[built command] #pragma config(Motor,port7,MOTOR_base_back_left,tmotorVex393_MC29,openLoop)
[built command] #pragma config(Motor,port8,MOTOR_base_right_all,tmotorVex393_MC29,openLoop)
[built command] #pragma config(Motor,port9,MOTOR_latch_motor,tmotorVex393_MC29,openLoop,reversed)
[built command] void GROUP_latch(float s){motor(MOTOR_latch_motor)=s;}
[built command] void GROUP_base_left(float s){motor(MOTOR_base_front_left)=s;motor(MOTOR_base_back_left)=s;}
[built command] void GROUP_base_right(float s){motor(MOTOR_base_right_all)=s;}
[built command] void GROUP_arm_unit(float s){motor(MOTOR_arm_right_upper)=s;motor(MOTOR_arm_right_lower)=s;motor(MOTOR_arm_left_upper)=s;motor(MOTOR_arm_left_lower)=s;}
[built command] void BIND_arm_unit(){if(vexRT[Btn6U]){GROUP_arm_unit(100.0);}else if(vexRT[Btn6D]){GROUP_arm_unit(-50.0);}else {GROUP_arm_unit(20.0);}}
[built command] void BIND_latch(){if(vexRT[Btn8D]){GROUP_latch(-25.0);}else if(vexRT[Btn8R]){GROUP_latch(25.0);}else {GROUP_latch(0.0);}}
[built command] void BIND_base_left(){GROUP_base_left(vexRT[Ch3]*1.0);}
[built command] void BIND_base_right(){GROUP_base_right(vexRT[Ch2]*1.0);}
[built command] autonomous code
[build autonomous] 4 steps, takes 3.0 seconds

 ===== END LOG ===== */

/* ===== SOURCE CODE =====

!* competition=True, tidy=True *!

define motor arm_right_upper {
	port 2,
	reversed
};
define motor arm_right_lower {
	port 3,
	reversed
};
define motor arm_left_upper {
	port 4
};
define motor arm_left_lower {
	port 5
};
define motor base_front_left {
	port 6
};
define motor base_back_left {
	port 7
};
define motor base_right_all {
	port 8
};
define motor latch_motor {
	port 9,
	reversed
};

group motor latch {
	latch_motor
};
group motor base_left {
	base_front_left,
	base_back_left
};
group motor base_right {
	base_right_all
};
group motor arm_unit {
	arm_right_upper,
	arm_right_lower,
	arm_left_upper,
	arm_left_lower
};

bind group arm_unit button {
	input 6U 100,
	input 6D -50,
	rest 20
};
bind group latch button {
	input 8D -25,
	input 8R 25
};
bind group base_left channel {
	input 3
};
bind group base_right channel {
	input 2
};

auton {
	run latch 25 500,
	run base_left base_right 100 1000,
	run arm_unit 100 500,
	run base_left base_right -100 1000
}
 ===== END CODE ===== */