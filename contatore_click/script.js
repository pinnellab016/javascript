const objContatore = document.querySelector("#contatore"); 
const objQuadrato = document.querySelector("#quadrato");

var contatore = 0;

function conta()
{
    contatore = contatore + 1;
    objContatore.innerHTML = "Contatore: " + contatore;

    if (contatore > 10)
    {
        objQuadrato.style.backgroundColor = "red"; 
    }
}

function reset()
{
    contatore = 0;
    objContatore.innerHTML = "Contatore: " + contatore;
    objQuadrato.style.backgroundColor = "greenyellow"; 
}

