var w = $('#tab-game').width();
var h = $('#tab-game').height();

var config = {
        type: Phaser.AUTO,
        width: w-20,
        height: h-20,
        parent: 'sc',
        physics: {
            default: 'arcade',
            arcade: {
                //gravity: { y: 0 }
            }
        },
        scene: {
            preload: preload,
            create: create,
            update: update
        }
    };


var ship;
var emitter;
var particles;
var deg;
var fuel = 1000;
var thrust = 100;
var mouseX;
var mouseY;
var xspeed
var yspeed
var angle;

var game = new Phaser.Game(config);


function preload (){
    //this.load.setBaseURL('http://labs.phaser.io');

    this.load.image('sky', '/static/assets/bg1.jpg');
    this.load.image('ship', '/static/assets/ship1.png');
    this.load.image('red', '/static/assets/fire.png');
    this.load.image('statusbar', '/static/assets/statusbar.png');
}

function create (){

    var image = this.add.image(this.cameras.main.width / 2, this.cameras.main.height / 2, 'sky');
    var sb = this.add.image(100, 100, 'statusbar');
    sb.displayWidth = w;
    sb.displayHeight = 300;

    let scaleX = this.cameras.main.width / image.width
    let scaleY = this.cameras.main.height / image.height
    let scale = Math.max(scaleX, scaleY)
    image.setScale(scale).setScrollFactor(0)

    particles = this.add.particles('red');

    emitter = particles.createEmitter({
        speed: 150,
        alpha: { start: 1, end: .2 },
        scale: { start: .11, end: 0 },
        blendMode: 'ADD',
        on: false
    });

    ship = this.physics.add.sprite(w/2, h/2, 'ship');
    ship.displayWidth = 22;
    ship.displayHeight = 42;
    ship.setVelocity(0, 0);
    ship.setBounce(1, 1);
    ship.setCollideWorldBounds(true);

    emitter.startFollow(ship);

    this.input.on('pointermove', function (pointer) {
        mouseX = pointer.x;
        mouseY = pointer.y;
        angle = Phaser.Math.Angle.Between(mouseX, mouseY, ship.x, ship.y) - Math.PI / 2;
        deg = angle*(180/Math.PI)+90;
        xspeed = thrust*Math.sin(angle);
        yspeed = thrust*Math.cos(angle)*-1;
        });

    this.input.on('pointerdown', function (pointer) {
        if(fuel > 0){
            emitter.on = true;
            ship.setAcceleration(xspeed, yspeed)
            };
    });

    this.input.on('pointerup', function (pointer) {
        emitter.on = false;
        ship.setAcceleration(0, 0);
    });

}

function update(){
    ship.setRotation(angle);
    if(emitter.on){fuel -= 1};
    emitter.setAngle({min: deg-5, max: deg+5});
}