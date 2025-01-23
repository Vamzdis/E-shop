function addToCart(productId) {
    if (!userLoggedIn) {

        window.location.href = `/login?next=/cart/add_to_cart/${productId}`;   
        return;
    }

    fetch(`/add_to_cart/${productId}`, {
        method: 'POST',
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