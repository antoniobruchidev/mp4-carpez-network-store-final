    $('.status-selector').on('change', function() {
        var orderId = $(this).data('id')
        $('.loading').removeClass("invisible")
        var form = $(`#status-${orderId}`)
        form.submit()
    })

    const delete_tag = async (tagId) => {
        var formData = new FormData()
        formData.append('csrfmiddlewaretoken', csrfToken)
        var url = `delete_tag/${tagId}`;
        try {
            const response = await fetch(url, {
                method: "POST",
                body: formData
            })

            const data = await response.json()
            if (data.success) {
                $(`#tag-${tagId}`).remove()
                createGreenToast(data)
            } else {
                createRedToast(data)
            }
            $('.loading').addClass("invisible")
        } catch(error) {
            console.log(error)
        }
    }

    const delete_category = async (categoryId) => {
        var formData = new FormData()
        formData.append('csrfmiddlewaretoken', csrfToken)
        var url = `delete_category/${categoryId}`;
        try {
            const response = await fetch(url, {
                method: "POST",
                body: formData
            })

            const data = await response.json()
            if (data.success) {
                $(`#category-${categoryId}`).remove()
                createGreenToast(data)
            } else {
                createRedToast(data)
            }
            $('.loading').addClass("invisible")
        } catch(error) {
            console.log(error)
        }
    }

    const delete_brand = async (brandId) => {
        var formData = new FormData()
        formData.append('csrfmiddlewaretoken', csrfToken)
        var url = `delete_brand/${brandId}`;
        try {
            const response = await fetch(url, {
                method: "POST",
                body: formData
            })

            const data = await response.json()
            if (data.success) {
                $(`#brand-${brandId}`).remove()
                createGreenToast(data)
            } else {
                createRedToast(data)
            }
            $('.loading').addClass("invisible")
        } catch(error) {
            console.log(error)
        }
    }

    const delete_discount = async (discountId) => {
        var formData = new FormData()
        formData.append('csrfmiddlewaretoken', csrfToken)
        var url = `delete_discount/${discountId}`;
        try {
            const response = await fetch(url, {
                method: "POST",
                body: formData
            })

            const data = await response.json()
            if (data.success) {
                $(`#discount-${discountId}`).remove()
                createGreenToast(data)
            } else {
                createRedToast(data)
            }
            $('.loading').addClass("invisible")
        } catch(error) {
            console.log(error)
        }
    }

    const createRedToast = (data) => {
        var toast = document.createElement("div")
        toast.classList.add("toast-error")
        toast.setAttribute("role", "alert")
        toast.setAttribute("id", "toast-error")
        var toastHeader = document.createElement("div")
        toastHeader.classList.add("toast-error-header")
        toastHeader.innerHTML = `
        <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 11.793a1 1 0 1 1-1.414 1.414L10 11.414l-2.293 2.293a1 1 0 0 1-1.414-1.414L8.586 10 6.293 7.707a1 1 0 0 1 1.414-1.414L10 8.586l2.293-2.293a1 1 0 0 1 1.414 1.414L11.414 10l2.293 2.293Z"/>
        </svg>
        <span class="sr-only">Error icon</span>
        `
        var message = document.createElement("div")
        message.classList.add("toast-error-message")
        message.innerText = data.error
        var button = document.createElement("button")
        button.classList.add("toast-error-dismiss")
        button.addEventListener("click", function (){
            var toast = button.parentElement
            toast.parentNode.removeChild(toast)
        })
        button.setAttribute("type", "button")
        button.setAttribute("aria-label", "Close")
        button.innerHTML = `
        <span class="sr-only">Close</span>
        <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
        </svg>
        `
        toast.appendChild(toastHeader)
        toast.appendChild(message)
        toast.append(button)
        var messageContainer = document.getElementById("messages")
        messageContainer.appendChild(toast)
    }

    const createGreenToast = (data) => {
        var toast = document.createElement("div")
                toast.classList.add("toast-success")
                toast.setAttribute("role", "alert")
                toast.setAttribute("id", "toast-success")
                var toastHeader = document.createElement("div")
                toastHeader.classList.add("toast-success-header")
                toastHeader.innerHTML = `
                <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z"/>
                </svg>
                <span class="sr-only">Check icon</span>
                `
                var message = document.createElement("div")
                message.classList.add("toast-success-message")
                message.innerText = data.success
                var button = document.createElement("button")
                button.classList.add("toast-success-dismiss")
                button.addEventListener("click", function (){
                    var toast = button.parentElement
                    toast.parentNode.removeChild(toast)
                })
                button.setAttribute("type", "button")
                button.setAttribute("aria-label", "Close")
                button.innerHTML = `
                <span class="sr-only">Close</span>
                <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
                </svg>
                `
                toast.appendChild(toastHeader)
                toast.appendChild(message)
                toast.append(button)
                var messageContainer = document.getElementById("messages")
                messageContainer.appendChild(toast)
    }

    const createTag = (data) => {
        var newTag = document.createElement("div")
        newTag.setAttribute("data-popover-target", `popover-tag-${data.new_tag_id}`)
        newTag.setAttribute("id", `tag-${data.new_tag_id}`)
        var newTagButton = document.createElement("div")
        newTagButton.setAttribute("id", `popover-tag-delete-${data.new_tag_id}`)
        newTagButton.setAttribute("data-tag-id", data.new_tag_id)
        newTagButton.classList.add("tag")
        newTagButton.innerText = data.new_tag_name
        var popoverTag = document.createElement("div")
        popoverTag.classList.add("tag-popover")
        var popoverTagHeader = document.createElement("div")
        popoverTagHeader.classList.add("tag-popover-header")
        var headerContent = document.createElement("h3")
        headerContent.classList.add("tag-popover-content")
        headerContent.innerText = "Click to delete"
        popoverTagHeader.appendChild(headerContent)
        popoverTag.appendChild(popoverTagHeader)
        popoverTag.setAttribute("data-popover", "")
        popoverTag.setAttribute("id", `popover-tag-${data.new_tag_id}`)
        popoverTag.setAttribute("role", "tooltip")
        var popoverContent = document.createElement("div")
        popoverContent.classList.add("px-3", "py-2")
        var p = document.createElement("p")
        p.classList.add("text-yellow-900")
        p.innerText = `Click to remove ${data.new_tag_name}`
        popoverContent.appendChild(p)
        var div = document.createElement("div")
        div.setAttribute("data-popover-arrow", "")
        newTag.appendChild(newTagButton)
        popoverTag.appendChild(popoverContent)
        popoverTag.appendChild(div)
        var tags = document.getElementById("tags")
        tags.appendChild(newTag)
        tags.appendChild(popoverTag)
        const $targetEl = popoverTag
        const $triggerEl = newTagButton

        // options with default values
        const options = {
            placement: 'top',
            triggerType: 'hover',
            offset: 10,
        };
        const popover = new Popover($targetEl, $triggerEl, options)
        return newTag
    }

    const createCategory = (data) => {
        var newCategory = document.createElement("div")
        newCategory.setAttribute("data-popover-target", `popover-tag-${data.new_category_id}`)
        newCategory.setAttribute("id", `category-${data.new_category_id}`)
        var newCategoryButton = document.createElement("div")
        newCategoryButton.setAttribute("id", `popover-category-delete-${data.new_category_id}`)
        newCategoryButton.setAttribute("data-category-id", data.new_category_id)
        newCategoryButton.classList.add("category")
        newCategoryButton.innerText = data.new_category_name
        var popoverCategory = document.createElement("div")
        popoverCategory.classList.add("category-popover")
        var popoverCategoryHeader = document.createElement("div")
        popoverCategoryHeader.classList.add("category-popover-header")
        var headerContent = document.createElement("h3")
        headerContent.classList.add("category-popover-content")
        headerContent.innerText = "Click to delete"
        popoverCategoryHeader.appendChild(headerContent)
        popoverCategory.appendChild(popoverCategoryHeader)
        popoverCategory.setAttribute("data-popover", "")
        popoverCategory.setAttribute("id", `popover-category-${data.new_category_id}`)
        popoverCategory.setAttribute("role", "tooltip")
        var popoverContent = document.createElement("div")
        popoverContent.classList.add("px-3", "py-2")
        var p = document.createElement("p")
        p.classList.add("text-yellow-900")
        p.innerText = `Click to remove ${data.new_category_name}`
        popoverContent.appendChild(p)
        var div = document.createElement("div")
        div.setAttribute("data-popover-arrow", "")
        newCategory.appendChild(newCategoryButton)
        popoverCategory.appendChild(popoverContent)
        popoverCategory.appendChild(div)
        var categories = document.getElementById("categories")
        categories.appendChild(newCategory)
        categories.appendChild(popoverCategory)
        const $targetEl = popoverCategory
        const $triggerEl = newCategoryButton

        // options with default values
        const options = {
            placement: 'top',
            triggerType: 'hover',
            offset: 10,
        };
        const popover = new Popover($targetEl, $triggerEl, options)
        return newCategory
    }

    const createBrand = (data) => {
        var newBrand = document.createElement("div")
        newBrand.setAttribute("data-popover-target", `popover-brand-${data.new_brand_id}`)
        newBrand.setAttribute("id", `brand-${data.new_brand_id}`)
        var newBrandButton = document.createElement("div")
        newBrandButton.setAttribute("id", `popover-brand-delete-${data.new_brand_id}`)
        newBrandButton.setAttribute("data-brand-id", data.new_brand_id)
        newBrandButton.classList.add("brand")
        newBrandButton.innerText = data.new_brand_name
        var popoverBrand = document.createElement("div")
        popoverBrand.classList.add("brand-popover")
        var popoverBrandHeader = document.createElement("div")
        popoverBrandHeader.classList.add("brand-popover-header")
        var headerContent = document.createElement("h3")
        headerContent.classList.add("brand-popover-header-content")
        headerContent.innerText = "Click to delete"
        popoverBrandHeader.appendChild(headerContent)
        popoverBrand.appendChild(popoverBrandHeader)
        popoverBrand.setAttribute("data-popover", "")
        popoverBrand.setAttribute("id", `popover-brand-${data.new_brand_id}`)
        popoverBrand.setAttribute("role", "tooltip")
        var popoverContent = document.createElement("div")
        popoverContent.classList.add("px-3", "py-2")
        var p = document.createElement("p")
        p.classList.add("text-yellow-900")
        p.innerText = `Click to remove ${data.new_brand_name}`
        popoverContent.appendChild(p)
        var div = document.createElement("div")
        div.setAttribute("data-popover-arrow", "")
        newBrand.appendChild(newBrandButton)
        popoverBrand.appendChild(popoverContent)
        popoverBrand.appendChild(div)
        var brands = document.getElementById("brands")
        brands.appendChild(newBrand)
        brands.appendChild(popoverBrand)
        const $targetEl = popoverBrand
        const $triggerEl = newBrandButton

        // options with default values
        const options = {
            placement: 'top',
            triggerType: 'hover',
            offset: 10,
        };
        const popover = new Popover($targetEl, $triggerEl, options)
        return newBrand
    }

    const createDiscount = (data) => {
        console.log("yes")
        var newDiscount = document.createElement("div")
        newDiscount.setAttribute("data-popover-target", `popover-discount-${data.new_discount_id}`)
        newDiscount.setAttribute("id", `discount-${data.new_discount_id}`)
        var newDiscountButton = document.createElement("div")
        newDiscountButton.setAttribute("id", `popover-discount-delete-${data.new_discount_id}`)
        newDiscountButton.setAttribute("data-discount-id", data.new_discount_id)
        newDiscountButton.classList.add("discount")
        newDiscountButton.innerText = data.new_discount_percentage
        var popoverDiscount = document.createElement("div")
        popoverDiscount.classList.add("discount-popover")
        var popoverDiscountHeader = document.createElement("div")
        popoverDiscountHeader.classList.add("discount-popover-header")
        var headerContent = document.createElement("h3")
        headerContent.classList.add("discount-popover-header-content")
        headerContent.innerText = "Click to delete"
        popoverDiscountHeader.appendChild(headerContent)
        popoverDiscount.appendChild(popoverDiscountHeader)
        popoverDiscount.setAttribute("data-popover", "")
        popoverDiscount.setAttribute("id", `popover-discount-${data.new_discount_id}`)
        popoverDiscount.setAttribute("role", "tooltip")
        var popoverContent = document.createElement("div")
        popoverContent.classList.add("px-3", "py-2")
        var p = document.createElement("p")
        p.classList.add("text-yellow-900")
        p.innerText = `Click to remove ${data.new_discount}`
        popoverContent.appendChild(p)
        var div = document.createElement("div")
        div.setAttribute("data-popover-arrow", "")
        newDiscount.appendChild(newDiscountButton)
        popoverDiscount.appendChild(popoverContent)
        popoverDiscount.appendChild(div)
        var discounts = document.getElementById("discount-container")
        discounts.appendChild(newDiscount)
        discounts.appendChild(popoverDiscount)
        const $targetEl = popoverDiscount
        const $triggerEl = newDiscountButton
        console.log(discounts, newDiscount)

        // options with default values
        const options = {
            placement: 'top',
            triggerType: 'hover',
            offset: 10,
        };
        const popover = new Popover($targetEl, $triggerEl, options)
        return newDiscount
    }

    $('.tag').on('click', async function() {
        var tagId = $(this).data('tag-id')
        delete_tag(tagId)
        
    })
    $('.category').on('click', function() {
        var categoryId = $(this).data('category-id')
        delete_category(categoryId)
        
    })
    $('.brand').on('click', function() {
        var brandId = $(this).data('brand-id')
        delete_brand(brandId)
    })
    $('.discount').on('click', function() {
        var discountId = $(this).data('discount-id')
        delete_discount(discountId)
    })
    $(".pagination-button").on("click", function(){
        var page = $(this).data("page")
        window.location.href = page
    })
    $('#add-tag').on("submit", async function(e) {
        e.preventDefault()
        var formData = new FormData(this)
        try {
            const response = await fetch("/dashboard/add_tag", {
                method: "POST",
                body: formData,
            })
            const data = await response.json()

            if (data.success) {
                createGreenToast(data)
                var newTag = createTag(data)
                newTag.addEventListener("click", async function() {
                    $('.loading').removeClass("invisible")
                    delete_tag(data.new_tag_id)
                })
            } else {
                createRedToast(data)
            }
        } catch (error) {
            
        }
    })
    $('#add-category').on("submit", async function(e) {
        e.preventDefault()
        var formData = new FormData(this)
        try {
            const response = await fetch("/dashboard/add_category", {
                method: "POST",
                body: formData,
            })
            const data = await response.json()
            if (data.success) {
            createGreenToast(data)
                var newCategory = createCategory(data)
                newCategory.addEventListener("click", async function() {
                    $('.loading').removeClass("invisible")
                    delete_category(data.new_category_id)
                })
            } else {
                createRedToast(data)
            }
        } catch (error) {
            console.log(error)
        }
    })
    $('#add-brand').on("submit", async function(e) {
        e.preventDefault()
        var formData = new FormData(this)
        try {
            const response = await fetch("/dashboard/add_brand", {
                method: "POST",
                body: formData,
            })
            const data = await response.json()

            if (data.success) {
                createGreenToast(data)
                var newBrand = createBrand(data)
                newBrand.addEventListener("click", async function() {
                    $('.loading').removeClass("invisible")
                    delete_brand(data.new_brand_id)
                })
            } else {
                createRedToast(data)
            }
        } catch (error) {
            
        }
    })
    $('#add-discount').on("submit", async function(e) {
        e.preventDefault()
        var formData = new FormData(this)
        try {
            const response = await fetch("/dashboard/add_discount", {
                method: "POST",
                body: formData,
            })
            const data = await response.json()

            if (data.success) {
                createGreenToast(data)
                var newDiscount = createDiscount(data)
                newDiscount.addEventListener("click", async function() {
                    $('.loading').removeClass("invisible")
                    delete_tag(data.new_disocunt_id)
                })
            } else {
                createRedToast(data)
            }
        } catch (error) {
            console.log(error)
        }
    })

    $(".review-answer").on("submit", async function (e) {
        e.preventDefault()
        var formData = new FormData(this)
        var reviewId = $(this).data("review")
        var url = `/reviews/answer_review/${reviewId}/`
        try {
            const response = await fetch(url,{
                method: "POST",
                body: formData,
            })
            const data = await response.json()
            if (data.success) {
                createGreenToast(data)
                $(`#review-${reviewId}`).remove()
            } else {
                createRedToast(data)
            }
        } catch (error) {
            console.log(error)
        }  
    })

    $(".send-email-from-review").on("click", function () {
        var email = $(this).data("email")
        window.open(`mailto:${email}`)
    })
    