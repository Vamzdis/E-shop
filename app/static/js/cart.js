function addToCart(productId) {
    if (!userLoggedIn) {
        alert("Please log in to add products to your cart.");

        // Redirecting to login page. Got to make sure the cart addition continues with add_to_cart route
        window.location.href = `/login?next=/cart/add_to_cart/${productId}`;   
        return;
    }

    fetch(`/add_to_cart/${productId}`, {
        // method: 'POST',.
        // headers: {
        //     'Content-Type': 'application/json',
        // },
    })
    .then(response => {
        if (response.ok) {
            alert("Product added to cart!");
        } else {
            alert("Failed to add product to cart.");
        }
    })
    .catch(error => {
        // should be proper error handling from user's perspective, should give him a popup or something
        console.error('Error:', error);
    });
}