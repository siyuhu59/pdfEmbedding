const searchInfo = {
    tablelist : [],
    selectedTable : '',
    searchValue : '',
    searchResult : [],
} 

const insertInfo = {
    selectedFile : '',
}

let loading = false;

document.addEventListener("DOMContentLoaded", function () {
    const searchTab = document.getElementById("search-tab");
    const insertTab = document.getElementById("insert-tab");
    const searchContent = document.getElementById("search-content");
    const insertContent = document.getElementById("insert-content");

    function setActiveTab(activeTab, inactiveTab, activeContent, inactiveContent) {
        activeTab.classList.add("text-gray-900", "border-b-2", "border-blue-500");
        activeTab.classList.remove("text-gray-500", "hover:bg-gray-100");

        inactiveTab.classList.add("text-gray-500", "hover:bg-gray-100");
        inactiveTab.classList.remove("text-gray-900", "border-b-2", "border-blue-500");

        activeContent.classList.remove("hidden");
        inactiveContent.classList.add("hidden");
    }

    searchTab.addEventListener("click", function () {
        setActiveTab(searchTab, insertTab, searchContent, insertContent);
    });

    insertTab.addEventListener("click", function () {
        setActiveTab(insertTab, searchTab, insertContent, searchContent);
    });
});


const addClickEvent = (id) => {
    const fileList = document.getElementById(`${id}-list`);

    fileList.addEventListener("click", function (event) {
        const clickedItem = event.target.closest(".p-3");

        if (!clickedItem) return; // 클릭한 요소가 .p-3이 아니면 무시
        // 나머지 아이템의 check 전부 제거
        const items = fileList.querySelectorAll(".p-3");
        items.forEach(function (item) {
            const checkIcon = item.querySelector("span.text-blue-500");
            if (checkIcon) {
                checkIcon.remove();
            }
            item.classList.remove("bg-blue-100");
        });

        // 체크 아이콘이 있는지 확인
        const checkIcon = clickedItem.querySelector("span.text-blue-500");

        if (checkIcon) {
            // 이미 체크된 경우 -> 체크 해제
            checkIcon.remove();
        } else {
            // 체크되지 않은 경우 -> 체크 추가
            const checkMark = document.createElement("span");
            checkMark.classList.add("text-blue-500");
            checkMark.innerHTML = "&#10003;";
            clickedItem.appendChild(checkMark);
            clickedItem.classList.add("bg-blue-100");
            if (id=='table') searchInfo.selectedTable = clickedItem.querySelector("span").innerText;
            if (id=='file') insertInfo.selectedFile = clickedItem.querySelector("span").innerText;
        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
    fetch('http://localhost:8000/files')
    .then(response => response.json())
    .then(data => {
        const fileList = document.getElementById("file-list");
        fileList.innerHTML = ``;
        data.files.forEach(function (file) {
            if(file == 'sqlite_sequence') return;
            const item = document.createElement("div");
            item.classList.add("p-3", "flex", "justify-between", "items-center", "border-b", "border-gray-200", "hover:bg-gray-100");
            item.innerHTML = `
                <div class="flex items-center">
                    <span class="text-lg">${file}</span>
                </div>
                `;
            fileList.appendChild(item);
        }
    )});
    // 위 이벤트가 끝나고 check 이벤트를 추가해야함
    addClickEvent('file');
});

document.addEventListener("DOMContentLoaded", function () {
    fetch('http://localhost:8000/tables')
    .then(response => response.json())
    .then(data => {
        const fileList = document.getElementById("table-list");
        fileList.innerHTML = ``;
        data.tables.forEach(function (file) {
            if(file == 'sqlite_sequence') return;
            const item = document.createElement("div");
            item.classList.add("p-3", "flex", "justify-between", "items-center", "border-b", "border-gray-200", "hover:bg-gray-100");
            item.innerHTML = `
                <div class="flex items-center">
                    <span class="text-lg">${file}</span>
                </div>
                `;
            fileList.appendChild(item);
        }
    )});
    // 위 이벤트가 끝나고 check 이벤트를 추가해야함
    addClickEvent('table');
});

document.addEventListener("DOMContentLoaded", function () {
    const searchButton = document.getElementById("searchbtn");
    const searchInput = document.getElementById("search");

    searchButton.addEventListener("click", function () {
        searchInfo.searchValue = searchInput.value;
        fetch(`http://localhost:8000/search?tablename=${searchInfo.selectedTable}&q=${searchInfo.searchValue}`)
        .then(response => response.json())
        .then(data => {
            searchInfo.searchResult = data.result;
            const searchResult = document.getElementById("search-result");
            searchResult.innerHTML = ``;
            const item = document.createElement("div");
            item.innerHTML = `
                <div class="p-3 border
                -b border-gray-200">
                    <div class="flex items
                    -center">
                        <span class="text-lg">${data.results}</span>
                    </div>
                </div>
                `;
            searchResult.appendChild(item);
            
        })
        .catch(error => {
            const searchResult = document.getElementById("search-result");
            searchResult.innerHTML = ``;
            const item = document.createElement("div");
            item.innerHTML = `
                <div class="p-3 border
                -b border-gray-200">
                    <div class="flex items
                    -center">
                        <span class="text-lg">No Result</span>
                    </div>
                </div>
                `;
            searchResult.appendChild(item);
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const insertButton = document.getElementById("insert-button");

    insertButton.addEventListener("click", function () {
        fetch(`http://localhost:8000/add_file?filename=${insertInfo.selectedFile}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
        });
    });
});