<script>
    //add to cart
    $(document).on('click', '#add-cart', function (e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: '{% url "cart_add" %}',
            data: {
                product_id: $('#add-cart').val(),
                product_qty: $('#qty-cart').val(),
                csrfmiddlewaretoken: '{{ csrf_token }}',
                action: 'post'
            },

            success: function (json) {
                //console.log(json)
                document.getElementById("cart_quantity").
                    textContent = json.qty
                location.reload()
            },
            error: function (xhr, errmsg, err) {

            }
        });
    })

    // script to update cart
    $(document).on('click', '.update-cart', function (e) {
        e.preventDefault();
        //grab the product id
        var productid = $(this).data('index');
        $.ajax({
            type: 'POST',
            url: '{% url "cart_update" %}',
            data: {
                product_id: $(this).data('index'),
                product_qty: $('#select' + productid).val(),
                csrfmiddlewaretoken: '{{ csrf_token }}',
                action: 'post'
            },

            success: function (json) {
                //console.log(json)
                //document.getElementById("cart_quantity").textContent = json.qty
                location.reload()
            },
            error: function (xhr, errmsg, err) {

            }
        });
    })

    // script to delete item from cart
    $(document).on('click', '.delete-cart-item', function (e) {
        e.preventDefault();
        //grab the product id
        //var productid = $(this).data('index');
        $.ajax({
            type: 'POST',
            url: '{% url "cart_delete" %}',
            data: {
                product_id: $(this).data('index'),
                csrfmiddlewaretoken: '{{ csrf_token }}',
                action: 'post'
            },

            success: function (json) {
                //console.log(json)
                //document.getElementById("cart_quantity").textContent = json.qty
                location.reload()
            },
            error: function (xhr, errmsg, err) {

            }
        });
    })

    // Lấy tham chiếu đến phần tử thông báo
    var notification = document.getElementById('messages');

    // Đặt opacity ban đầu là 1
    notification.style.opacity = 1;

    // Tính toán số lần lặp để đạt được opacity 0 trong 5 giây (1000ms * 5 = 5000ms)
    var numIntervals = 70;
    var intervalDuration = 100;

    // Tính toán sự thay đổi của opacity trong mỗi lần lặp
    var opacityChange = 1 / numIntervals;

    // Thiết lập interval để thay đổi opacity mỗi intervalDuration ms
    var fadeEffect = setInterval(function() {
        // Nếu opacity đã đạt đến 0, dừng interval và ẩn phần tử
        if (notification.style.opacity <= 0) {
            clearInterval(fadeEffect);
            notification.style.display = 'none';
        } else {
            // Giảm opacity đi opacityChange trong mỗi lần lặp
            notification.style.opacity -= opacityChange;
        }
    }, intervalDuration); // intervalDuration ms

</script>