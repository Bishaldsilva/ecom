var updatebtn = document.getElementsByClassName('update-cart')
for(var i=0;i<updatebtn.length;i++){
    updatebtn[i].addEventListener('click',function(){
        var prodid = this.dataset.product
        var action = this.dataset.action
        console.log('ProductId:',prodid,'Action:',action)
        console.log('USER:',user)
        if(user === 'AnonymousUser'){
            addCookieItem(prodid,action)
        }
        else(
            updateUserOrder(prodid,action)
        )
    })
}

function addCookieItem(productId,action){
    if(action =='add'){
        if(cart[productId] == undefined){
            cart[productId] = {'quantity':1}
        }else{
            cart[productId]['quantity'] += 1
        }
    }
    if(action =='remove'){
        cart[productId]['quantity'] -= 1
        if(cart[productId]['quantity'] <= 0){
            delete cart[productId]
        }
    }
    console.log('cart:',cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}

function updateUserOrder(productid,action){
    var url = '/update_item/'
    fetch(url,{
        method:'POST',
        headers:{
            'content-type':'application/json',
            'X-CSRFToken': csrftoken
        },
        body:JSON.stringify({'productId':productid,'action':action})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) =>{
        console.log(data)
        location.reload()
    })
}