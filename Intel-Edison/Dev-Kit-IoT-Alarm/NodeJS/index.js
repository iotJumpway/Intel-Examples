////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2016 TechBubble Technologies and other Contributors.
//
// All rights reserved. This program and the accompanying materials
// are made available under the terms of the Eclipse Public License v1.0
// which accompanies this distribution, and is available at
// http://www.eclipse.org/legal/epl-v10.html 
//
// Contributors:
//   Adam Milton-Barker - TechBubble Technologies Limited
////////////////////////////////////////////////////////////////////////////////

var mqtt    = require('mqtt');
var fs = require('fs');
const mraa = require('mraa'); 
var config = require(__dirname + '/config.json');
var TRUSTED_CA_LIST = fs.readFileSync(__dirname + '/certs/ca.pem');

var options = {
	protocol: 'mqtts',    
	protocolId: 'MQIsdp',
	secureProtocol: 'TLSv1_method',
	protocolVersion: 3,
	certPath: TRUSTED_CA_LIST,
	host: config.IoTJumpWayMQTTSettings.host,
	port: config.IoTJumpWayMQTTSettings.port,
	clientId: config.IoTJumpWaySettings.SystemDeviceName,
	username: config.IoTJumpWayMQTTSettings.dUsername,
	password: config.IoTJumpWayMQTTSettings.dPassword,
	will: {
		topic: config.IoTJumpWaySettings.SystemLocation+'/Devices/'+config.IoTJumpWaySettings.SystemZone+'/'+config.IoTJumpWaySettings.SystemDeviceID+'/Status',
		payload: "OFFLINE"
	}
};

var ledOKPin = new mraa.Gpio(config.Actuators.LED.PIN); 
var ledWarnPin = new mraa.Gpio(config.Actuators.LED2.PIN); 
var ledAlarmPin = new mraa.Gpio(config.Actuators.Buzzer.PIN); 

ledOKPin.dir(mraa.DIR_OUT); 
ledWarnPin.dir(mraa.DIR_OUT); 
ledAlarmPin.dir(mraa.DIR_OUT); 

var client = mqtt.connect(options)

client.subscribe(config.IoTJumpWaySettings.SystemLocation+'/Devices/'+config.IoTJumpWaySettings.SystemZone+'/'+config.IoTJumpWaySettings.SystemDeviceID+'/Commands')
client.on('message', function (topic, message) {
	data = JSON.parse(message.toString());
	if(data.ActuatorID==131){
		console.log("Turn On OK LED")
		ledOKPin.write(1);
		setTimeout(function() {
			console.log("Turn Off OK LED")
			ledOKPin.write(0);
		}, 3000);
	}
	if(data.ActuatorID==132){
		console.log("Turn On Warning LED")
		ledWarnPin.write(1);
		setTimeout(function() {
			console.log("Turn Off Warning LED")
			ledWarnPin.write(0);
		}, 3000);
	}
	if(data.ActuatorID==133){
		ledAlarmPin.write(1);
		setTimeout(function() {
			console.log("Turn Off Buzzer")
			ledAlarmPin.write(0);
		}, 3000);
	}
	
})

client.on('error', function (err) {
  console.log(JSON.stringify(err))
})

client.on('connect', function () {
	console.log('Connected To TechBubble IoT JumpWay')
  client.publish(config.IoTJumpWaySettings.SystemLocation+'/Devices/'+config.IoTJumpWaySettings.SystemZone+'/'+config.IoTJumpWaySettings.SystemDeviceID+'/Status', "ONLINE")
})