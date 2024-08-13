export default{
    template:`
    <div class="fixed-sidebar">
        <ul class="nav flex-column mb-1">
            <li class="nav-item" style="display: flex; flex-direction: column; align-items: center; text-align: center;" >
                <img class="sidebar-icon" src="./static/assets/notes.png" alt="Modules Icon" style="width:45px">
                <a class="nav-link" href="#">Modules</a>
            </li>
            <li class="nav-item" style="display: flex; flex-direction: column; align-items: center; text-align: center;" >
                <img class="sidebar-icon" src="./static/assets/report_card.png" alt="Grades Icon" style="width:45px">
                <a class="nav-link" href="#">Grades</a>
            </li>
            <li class="nav-item" style="display: flex; flex-direction: column; align-items: center; text-align: center;" >
                <img class="sidebar-icon" src="./static/assets/inbox.png" alt="Inbox Icon" style="width:45px">
                <a class="nav-link" href="#">Inbox <span class="badge bg-secondary">17</span></a>
            </li>
            <li class="nav-item" style="display: flex; flex-direction: column; align-items: center; text-align: center;" >
                <img class="sidebar-icon" src="./static/assets/discuss.png" alt="Discuss Icon" style="width:45px">
                <a class="nav-link" href="#">Discuss</a>
            </li>
            <li class="nav-item" style="display: flex; flex-direction: column; align-items: center; text-align: center;" >
                <img class="sidebar-icon" src="./static/assets/calculator.png" alt="Calculator Icon" style="width:45px">
                <a class="nav-link" href="#">Calc</a>
            </li>
        </ul>
    </div>
    `
}