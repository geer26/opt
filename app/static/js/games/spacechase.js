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
var fuel = 100;
var thrust = 100;
var mouseX;
var mouseY;
var xspeed
var yspeed
var angle;
var bar_bar;

var game = new Phaser.Game(config);


function preload (){
    //this.load.setBaseURL('http://labs.phaser.io');

    this.load.image('sky', '/static/assets/bg1.jpg');
    this.load.image('ship', '/static/assets/ship1.png');
    this.load.image('red', '/static/assets/fire.png');
    this.load.image('bar', '/static/assets/bar_bar.png');
    this.load.image('statusbar', '/static/assets/bar_foreground.png');
}

function create (){

    var image = this.add.image(this.cameras.main.width / 2, this.cameras.main.height / 2, 'sky');

    var bar_bar = this.add.image(10, -3, 'bar').setOrigin(0,0);
    bar_bar.displayWidth = 26;
    bar_bar.displayHeight = h;

    var sb = this.add.image(10, 0, 'statusbar').setOrigin(0,0);
    sb.displayWidth = 30;
    sb.displayHeight = h;

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
            ship.setAcceleration(xspeed, yspeed);
            bar_bar.scaleY *= fuel/100;
            }
            else{
            bar_bar.visible = false;
            };
    });

    this.input.on('pointerup', function (pointer) {
        emitter.on = false;
        ship.setAcceleration(0, 0);
    });

}

function update(){
    ship.setRotation(angle);
    if(emitter.on){
        fuel -= .1;
        };
    emitter.setAngle({min: deg-5, max: deg+5});
}