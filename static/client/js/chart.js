var piechart=document.getElementById('projectprogress').getContext('2d');

    function dynamicColors() {
        var r = Math.floor(Math.random() * 255);
        var g = Math.floor(Math.random() * 255);
        var b = Math.floor(Math.random() * 255);
        return "rgba(" + r + "," + g + "," + b + ", 0.5)";
    }
    function poolColors(a) {
        var pool = [];
        for(i = 0; i < a; i++) {
            pool.push(dynamicColors());
        }
        return pool;
    }

    var x = new Chart(piechart, {
            "type":"doughnut",
            "data":{
                "labels":[
                    {% for i in data4%}
                    "{{i.scope_of_work}}",
                    {% endfor %}
                ],
                "datasets":[{
                    "label":"My First Dataset",
                    "data":[
                        {% for i in data4 %}
                        {{i.level}},
                        {% endfor %}
                    ],
                    "backgroundColor":poolColors(6),
                    "borderColor": poolColors(6),
                    "border":1,
                }]
            }
        }
    );