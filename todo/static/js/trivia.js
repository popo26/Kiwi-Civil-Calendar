function checkAnswer1(){
    const answer = document.getElementById('answer').value;
    const trues = document.getElementById('trues')
    let true_text = trues.getAttribute('name')
    const q_img = document.getElementById('question-img')
       
    if (answer != true_text){
        document.getElementById('result').innerHTML = "WRONG!";
        document.getElementById('result').style.color = "red";
        q_img.src = "https://media.giphy.com/media/JT7Td5xRqkvHQvTdEu/giphy.gif";
    } else {
        document.getElementById('result').innerHTML = "CORRECT!";
        document.getElementById('result').style.color = "green";
        q_img.src= "https://media.giphy.com/media/fE9BG83QDphzkYoHr9/giphy.gif"
    };
    
};

function checkAnswer2(){
    const answer = document.getElementById('answer').value;
    const falses = document.getElementById("falses")
    let false_text = falses.getAttribute('name')
    const q_img = document.getElementById('question-img')
   
    
    if (answer != false_text){
        document.getElementById('result').innerHTML = "WRONG!";
        document.getElementById('result').style.color = "red";
        q_img.src = "https://media.giphy.com/media/JT7Td5xRqkvHQvTdEu/giphy.gif";
    } else {
        document.getElementById('result').innerHTML = "CORRECT!"
        document.getElementById('result').style.color = "green"
        q_img.src = "https://media.giphy.com/media/fE9BG83QDphzkYoHr9/giphy.gif"
    };
    
};