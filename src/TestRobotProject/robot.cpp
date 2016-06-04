#include "WPILib.h"
#include <iostream>

class CommandBasedRobot : public IterativeRobot {
private:
    RobotDrive *drive;
    Joystick *stick;
private:

	virtual void RobotInit() {
		cout << "Init\n";
		this->drive = new RobotDrive(2,1);
		this->drive->SetSafetyEnabled(false);
		this->drive->SetInvertedMotor(RobotDrive::kRearLeftMotor, true);
        this->drive->SetInvertedMotor(RobotDrive::kRearRightMotor, false);

		this->stick = new Joystick(1);
	}

	virtual void AutonomousInit() {
		cout << "Auto Init" << DriverStation::GetInstance()->GetPacketNumber() << " " << Timer::GetPPCTimestamp();
	}

	virtual void AutonomousPeriodic() {
		cout << "Auto Periodic " << DriverStation::GetInstance()->GetPacketNumber() << " " << Timer::GetPPCTimestamp() << endl;
	}

	virtual void TeleopInit() {
		cout << "Teleop Init " << DriverStation::GetInstance()->GetPacketNumber() << " " << Timer::GetPPCTimestamp() << endl;
	}

	virtual void TeleopPeriodic() {
		cout << "Teleop Periodic " << DriverStation::GetInstance()->GetPacketNumber() << " " << Timer::GetPPCTimestamp() << endl;
		this->drive->ArcadeDrive(this->stick);
	}

	virtual void TestPeriodic() {
		cout << "Teleop Periodic" << DriverStation::GetInstance()->GetPacketNumber() << " " << Timer::GetPPCTimestamp() << endl;
	}

	virtual void DisabledInit() {
		cout << "Disabled Periodic" << DriverStation::GetInstance()->GetPacketNumber() << " " << Timer::GetPPCTimestamp() << endl;
	}

	virtual void DisabledPeriodic() {
		cout << "Disabled Periodic" << DriverStation::GetInstance()->GetPacketNumber() << " " << Timer::GetPPCTimestamp() << endl;
	}
};

START_ROBOT_CLASS(CommandBasedRobot);
