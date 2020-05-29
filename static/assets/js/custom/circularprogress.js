var c4 = $('.forth.circle');
var x = $('.forth.circle').attr('data-value');
var y = x/100
c4.circleProgress({
    startAngle: -Math.PI / 4 * 3,
    value: y,
    lineCap: 'round',
    fill: {gradient: [['#0681c4', .6], ['#4ac5f8', .4]], gradientAngle: Math.PI / 4}
}).on('circle-animation-progress', function(event, progress, value) {
    $(this).find('strong').html(Math.round(100 * value) + '<i>%</i>')
});

if(x){
    animate();
}

function animate(){
    setTimeout(function() { c4.circleProgress('value', y); }, 1000);
    setTimeout(function() { c4.circleProgress('value', 1.0); }, 1100);
    setTimeout(function() { c4.circleProgress('value', y); }, 2100);
}