document.addEventListener('DOMContentLoaded', function () {

    document.querySelector('#yearlyFrame').addEventListener('click', () => checkProgressPercent('yearly'));
    document.querySelector('#monthlyFrame').addEventListener('click', () => checkProgressPercent('monthly'));
    document.querySelector('#weeklyFrame').addEventListener('click', () => checkProgressPercent('weekly'));
    document.querySelector('#dailyFrame').addEventListener('click', () => checkProgressPercent('daily'));
    
    // Stores Time Frame in session storage (cache)
    const defaultTicker = sessionStorage.getItem('localTicker') || 'yearly';

    var currentTickerValue = defaultTicker;
    console.log(currentTickerValue)

    const updateSessionStorage = () => {
        sessionStorage.setItem('localTicker', currentTickerValue);
    };

    window.addEventListener('load', () => {
        toDoListFilter1(defaultTicker)
    })

    const options = {
        year: 'numeric', month: 'long', day: 'numeric',
        hour: 'numeric', minute: 'numeric', second: 'numeric'
    };

    const clock = () => {
        const dateTime = document.getElementById('dateTime');
        dateTime.innerText = new Intl.DateTimeFormat('en-EN', options).format(new Date());
    };
    
    clock();
    setInterval(clock, 1000);

    // A class that handles all Time Frame percentage calculations
    class timeFrameCalculator {
        constructor(date = new Date()) {
            this.date = date
            this.oneDay = 1000 * 60 * 60 * 24;

            // Year ticker
            this.timePassedMsYear = this.date - this.getPercentDayOfYear().prevYear;
            
            // Month ticker
            this.timePassedMsMonth = this.date - this.getPercentDayOfMonth().lastMonth;
            
            // Weekly ticker
            this.timePassedMsWeek = this.getPercentDayOfWeek().thisWeekMs + this.getPercentDayOfWeek().daysInDays;

            // Day ticker
            this.timePassedMsDay = this.date - this.getPercentDay()

        }

        yearMsIncrement() {
            this.timePassedMsYear += 1000;
        }

        monthMsIncrement() {
           this.timePassedMsMonth += 1000;
        }

        weekMsIncrement() {
            this.timePassedMsWeek += 1000;
        }
        
        DayMsIncrement() {
            this.timePassedMsDay += 1000;
        }

        // Year time frame calculation
        getPercentDayOfYear() {
            const prevYear = new Date(this.date.getFullYear(), 0, 1);
            const currentYear = new Date(this.date.getFullYear() + 1, 0, 1)
            const totalDaysYearMs = currentYear - prevYear
            
            return {
                prevYear,
                currentYear,
                totalDaysYearMs,
            }
        }

        // Month time frame calculation
        getPercentDayOfMonth() {
            const lastMonth = new Date(this.date.getFullYear(), this.date.getMonth(), 1);
            const currentMonth = new Date(this.date.getFullYear(), this.date.getMonth() + 1, 1)
            const daysInMonthMs = currentMonth - lastMonth;
            let timePassedMsMonth = this.date - lastMonth;
            const progressPercentMonthly = (timePassedMsMonth / daysInMonthMs) * 100;
        
            return {
                lastMonth,
                currentMonth,
                daysInMonthMs,
            }
        }   

        // Week time frame calculation
        getPercentDayOfWeek() {
            //Javascript default 0 is Sunday, 6 is Saturday
            const defaultDayIndex = this.date.getDay()
            // make monday first day of the week and sunday the last day
            // monday will be index 0, and sunday will be index 6
            const today = defaultDayIndex === 0 ? 6 : defaultDayIndex - 1;
            const thisWeekMs = (today * this.oneDay)
            const totalDaysInWeekMs = 7 * this.oneDay
            const daysInWeekPercentMs = thisWeekMs / totalDaysInWeekMs
            const daysInDays = (this.date - new Date(this.date.getFullYear(), this.date.getMonth(), this.date.getDate()));

            return {
                daysInDays,
                today,
                thisWeekMs,
                totalDaysInWeekMs,
                daysInWeekPercentMs,
            }
        }

        // Daily time frame calculation
        getPercentDay() {
            const timePassedMsDay = new Date(this.date.getFullYear(), this.date.getMonth(), this.date.getDate())   
            return timePassedMsDay
        }
    }
    
    const progressPercentage = (timeFrame) => {
        // A variable to hold timeFrame's value
        var progressPercent;

        switch (timeFrame) {
            case 'yearly':
                currentTickerValue = 'yearly';
                sessionStorage.setItem('localTicker', currentTickerValue);
                progressPercent = (calculator.timePassedMsYear / calculator.getPercentDayOfYear().totalDaysYearMs) * 100;
                calculator.yearMsIncrement();
                break

            case 'monthly':
                currentTickerValue = 'monthly';
                sessionStorage.setItem('localTicker', currentTickerValue);
                progressPercent = (calculator.timePassedMsMonth / calculator.getPercentDayOfMonth().daysInMonthMs) * 100;
                // console.log(calculator.getPercentDayOfMonth());
                calculator.monthMsIncrement();
                break

            case 'weekly':
                currentTickerValue = 'weekly';
                sessionStorage.setItem('localTicker', currentTickerValue);
                progressPercent = (calculator.timePassedMsWeek / calculator.getPercentDayOfWeek().totalDaysInWeekMs) * 100;
                // console.log(calculator.getPercentDayOfWeek());
                calculator.weekMsIncrement();
                break

            case 'daily':
                currentTickerValue = 'daily';
                sessionStorage.setItem('localTicker', currentTickerValue);
                progressPercent = calculator.timePassedMsDay / (1 * calculator.oneDay) * 100;
                // console.log(calculator.getPercentDay());
                calculator.DayMsIncrement();
                break
        }
        updateProgressBar(progressPercent);
        // console.log(currentTickerValue);
        // console.log(progressPercent);
        updateSessionStorage();
        // console.log(sessionStorage.localTicker);
        return progressPercent;
    };

    const checkProgressPercent = (timeFrame) => {
        if (timeFrame !== currentTickerValue) {
            updateTimeFrameName(timeFrame);
            toDoListFilter1(timeFrame);
            toDoListCounter = 1;
            return progressPercentage(timeFrame);
        }
        // updateTimeFrameName(timeFrame)
        // toDoListFilter(timeFrame)
        // return timeFrame !== currentTickerValue ? progressPercentage(timeFrame) : undefined;
    }

    // Sets the number of decimal places
    function updateProgressBar(progressPercent) {
        const progressCounter = document.getElementById('progressCounter');
        progressCounter.innerText = progressPercent.toFixed(6) + ' %';
        progressCounter.style.width = progressPercent + '%';
    }

    // Updates the name of Time Frame 
    function updateTimeFrameName(currentTickerValue) {
        const timeFrameName = document.getElementById('timeFrame');
        if (currentTickerValue === 'weekly') {
            timeFrameName.innerText = currentTickerValue + " percentage";
        } else {
            timeFrameName.innerText = currentTickerValue + " percentage";
        }
    }

    const calculator = new timeFrameCalculator();
    // console.log(calculator.timePassedMsWeek);
    progressPercentage(currentTickerValue);
    updateTimeFrameName(currentTickerValue);
    setInterval(() => progressPercentage(currentTickerValue), 1000);
    
    // function days_of_a_year(year) {
    //     return isLeapYear(year) ? 366 : 365;
    // };

    // function isLeapYear(year) {
    //     return year % 400 === 0 || (year % 100 !== 0 && year % 4 === 0);
    // };
    
    document.addEventListener('click', function(event) {
        let toDoListButton = document.getElementById('addToDoListButton');
        let textBox = document.getElementById('addToDoListInput');

        if (event.target !== textBox && !textBox.contains(event.target)) {
            textBox.style.display = 'none'; 
        }
        if (event.target == toDoListButton) {
            addToDoList(event);
        }
    });

    function addToDoList(event) {
        event.stopPropagation();
        var textBox = document.getElementById('addToDoListInput');
        textBox.style.display = 'inline-block';
        textBox.placeholder = "Hit 'Enter' to submit";
        textBox.focus();

        textBox.addEventListener("keyup", function(event) {
            if (event.key === "Enter") {
                createListItem(textBox.value.trim());
                textBox.value = "";
                textBox.style.display = "none";
            }
        });
    };

    function createListItem(text) {
        if (text !== null && text !== undefined && text !== "") {
            // Creating a list item does not have a key
            var key = undefined;
            // Create three table data cells
            creatingTable(text);       
            makeFetchAPICallPost(text);

        }
    };

    function makeFetchAPICallPost(data) {
        fetch(`/create_post`, {
            method: 'POST',
            body: JSON.stringify({
                post: data,
                timeline: currentTickerValue,
            })
        });
    }

    var toDoListCounter = 1;
    function creatingTable(text) {
        var table = document.querySelector('.table-hover');
        table.style.display = '';
        // Create three table data cells
        var row = document.createElement('tr');
        row.dataset.id = toDoListCounter;
        toDoListCounter ++;

        var col1 = document.createElement('td');
        addTickButton(col1);

        var col2 = document.createElement('td');
        col2.textContent = text;

        var col3 = document.createElement('td');
        addDeleteButton1(table, col3);

        row.appendChild(col1);
        row.appendChild(col2);
        row.appendChild(col3);

        table.appendChild(row);

        return col2;
    }

    function addTickButton(element) {
        var tickButton = document.createElement("button");
        const table = document.querySelector('.table-hover');
        tickButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="green" class="bi bi-check2" viewBox="0 0 16 16"><path d="M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0"></path></svg>';
        tickButton.classList.add('btn', 'btn-sm', 'btn-outline-success');

        tickButton.addEventListener('click', () => {
            var tr = element.parentNode
            complete_status = true
            makeFetchAPICallPUT(tr, complete_status);
            removeTableRowItem(table, element);
            completedTableRowItem(tr.querySelector('td:nth-child(2)'));
            
        })
        element.appendChild(tickButton);

    }

    function completedTableRowItem(td_col2 = null) {
        var success_badge = '<button class="badge badge-success">Completed</button>'
        const undo_button = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-counterclockwise" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 3a5 5 0 1 1-4.546 2.914.5.5 0 0 0-.908-.417A6 6 0 1 0 8 2z"/><path d="M8 4.466V.534a.25.25 0 0 0-.41-.192L5.23 2.308a.25.25 0 0 0 0 .384l2.36 1.966A.25.25 0 0 0 8 4.466"/></svg>'
        // removeTableRowItem(element);

        completed_table = document.querySelector('.table-hover-complete');
        completed_table.style.display = '';
        // tr = element.parentNode // Get the parent table row (tr)
        // td_col2 = tr.querySelector('td:nth-child(2)'); // Get the second td element in the row
        
        var row = document.createElement('tr');

        var col1 = document.createElement('td');
        col1.innerHTML = success_badge;

        var col2 = document.createElement('td');
        col2.innerHTML = td_col2.textContent ? td_col2.textContent : td_col2; // Check if td_col2 is provided

        var col3 = document.createElement('td');
        addUndoButton(col3)

        row.appendChild(col1);
        row.appendChild(col2);
        row.appendChild(col3);
        completed_table.appendChild(row);
    }

    function incompleteTableRowItem(item) {
        incomplete_table = document.querySelector('.table-hover-incomplete');
        incomplete_table.style.display = '';

        var row = document.createElement('tr');

        var col1 = document.createElement('td');
        col1.textContent = item;

        row.appendChild(col1);
        incomplete_table.appendChild(row);
    }

    function addUndoButton(element) {
        table = document.querySelector('.table-hover-complete');
        var undoButton = document.createElement("button");
        undoButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-counterclockwise" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 3a5 5 0 1 1-4.546 2.914.5.5 0 0 0-.908-.417A6 6 0 1 0 8 2z"/><path d="M8 4.466V.534a.25.25 0 0 0-.41-.192L5.23 2.308a.25.25 0 0 0 0 .384l2.36 1.966A.25.25 0 0 0 8 4.466"/></svg>'
        undoButton.classList.add('btn', 'btn-sm', 'btn-warning');

        element.appendChild(undoButton);
        
        undoButton.addEventListener('click', () => {
            var tr = element.parentNode;
            td_col2 = tr.querySelector(':nth-child(2)').textContent;
            complete_status = false;
            
            removeTableRowItem(table, element);
            creatingTable(td_col2);
            makeFetchAPICallPUT(tr, complete_status);
        });
    }

    function addDeleteButton1(table, element) {
        table = document.querySelector('.table-hover');

        var deleteButton = document.createElement("button");
        deleteButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3" viewBox="0 0 16 16"><path d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5M11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47M8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5"/></svg>';
        deleteButton.classList.add('btn', 'btn-sm', 'btn-outline-danger');

        deleteButton.addEventListener('click', () => {
            removeTableRowItem(table, element);
            var tr = element.parentNode
            makeFetchAPICallDELETE(tr);
        });

        element.appendChild(deleteButton);
    }

    function removeTableRowItem(table, element) {
        tr = element.parentNode;
        console.log(table);
        // table = document.querySelector('.table-hover');
        table.removeChild(tr);
    }

    function makeFetchAPICallDELETE(element) {
        fetch(`/delete_post`, {
            method: 'DELETE',
            body: JSON.stringify({
                post: element.querySelector(':nth-child(2)').textContent,
                timeline: currentTickerValue,
            })
        })
    }

    function makeFetchAPICallPUT(element, complete_status) {
        fetch(`/update_post`, {
            method: 'PUT',
            body: JSON.stringify({
                post: element.querySelector(':nth-child(2)').textContent,
                completion: complete_status,
                timeline: currentTickerValue,
            })
        })
    }

    function timeFrameIdentifier(startToEndDate) {
        const incomplete = document.querySelector('.todo-status-incomplete');
        console.log(incomplete);
        incomplete.textContent += ' (' + startToEndDate + ')';
    }

    function toDoListFilter1(timeFrame) {
        const tableHover = document.querySelector(".table-hover");
        tableHover.innerHTML = "";

        const tableHoverComplete = document.querySelector(".table-hover-complete");
        tableHoverComplete.innerHTML = "";

        const tableHoverIncomplete = document.querySelector(".table-hover-incomplete");
        tableHoverIncomplete.innerHTML = "";

        const startToEndTimeFrame = document.querySelector(".todo-status-incomplete");
        startToEndTimeFrame.innerHTML = "UNCOMPLETED";

        fetch(`timeFrame/${timeFrame}`)
            .then(response => response.json())
            .then(data => {
                console.log(data)

                // In Progress To-Do-List
                var timeFrameArray = []
                // Completed To-Do-List
                var completedArray = []
                // Incomplete To-Do-List
                var incompleteArray = []
                // Array for start and end date
                var startToEndTimeFrame = []

                for (const key in data) {
                    if (key === timeFrame) {
                        timeFrameArray.push(data[key]);
                    } else if (key === 'completed') {
                        completedArray.push(data[key]);
                    } else if (key === 'incomplete') {
                        incompleteArray.push(data[key])
                    } else if (key === 'start_to_end') {
                        startToEndTimeFrame.push(data[key])
                    }
                    console.log(data[key])
                }
                console.log(timeFrameArray);
                console.log(completedArray);
                console.log(incompleteArray);
                console.log(startToEndTimeFrame);

                timeFrameArray.forEach(array => {
                    array.forEach(item => {
                        console.log(item);
                        creatingTable(item);
                    })
                });
                completedArray.forEach(array => {
                    array.forEach(item => {
                        console.log(item);
                        completedTableRowItem(item);
                    });
                });
                incompleteArray.forEach(array => {
                    array.forEach(item => {
                        console.log(item);
                        incompleteTableRowItem(item);
                    })
                })
                timeFrameIdentifier(startToEndTimeFrame[0]);
                // const incomplete = document.querySelector('.todo-status-incomplete');
                // const startToEnd = startToEndTimeFrame[0];
                // incomplete.textContent += '(' + startToEnd + ')';

            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
});


