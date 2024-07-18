$(document).ready(function(){

    var items = [];
    $('#checkoutbutton').on("click", addItemTosales);
    $('#sales-table').on("click", ".btn-danger", removeItemFromCart);

    function addItemTosales(event){
        event.preventDefault();

        sales_count = 0;
        var itemName = "Sales " + sales_count 
        var itemPrice = parseFloat($("#total-cost").val());

        if(itemName !== "" && !isNaN(itemPrice)){
            var item = {
                name: itemName,
                price: itemPrice
            };

            items.push(item);
            var index = items.length - 1;

            $("#cart-table tbody").append(
                "<tr data-index='" + index + "'><td>" + item.name + "</td><td>₹" + item.price.toFixed(2) + "</td><td><button class='btn btn-sm btn-danger'><i class='bi bi-x'></i></button></td></tr>"
            );

            // updateTotalCost();
            // $("#productName").val("");
            // $("#productPrice").val("");
            // $("#productDiscount").val("");
        }
    }

    function removeItemFromCart(){
        var index = $(this).closest("tr").data('index');
        items.splice(index, 1);
        $(this).closest("tr").remove();
        updateCartTable();
        updateTotalCost();
    }

    function updateCartTable(){
        $("#sales-table tbody").empty();
        items.forEach(function(item, index){
            $("#sales-table tbody").append(
                "<tr data-index='" + index + "'><td>" + item.name + "</td><td>₹" + item.price.toFixed(2) + "</td><td>₹" + item.discount.toFixed(2) + "</td><td>₹" + item.total.toFixed(2) + "</td><td><button class='btn btn-sm btn-danger'><i class='bi bi-x-md'></i></button></td></tr>"
            );
        });
    }

    // function updateTotalCost(){
    //     var totalCost = 0;
    //     items.forEach(function(item){
    //         totalCost += item.total;
    //     });

    //     $("#total-cost").text(" ₹" + totalCost.toFixed(2));
    // }

});