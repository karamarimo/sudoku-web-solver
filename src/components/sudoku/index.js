import { h, Component } from 'preact';
import style from './style';
import axios from 'axios'

export default class Sudoku extends Component {
    constructor() {
        super();

        const data = [];
        for (let i = 0; i < 9; i++) {
            let row = [];
            for (let j = 0; j < 9; j++) {
                row.push(0);
            }
            data.push(row);
        }
        this.state = {
            data
        };
        this.onChangeAt = this.onChangeAt.bind(this);
    }

    // gets called when this route is navigated to
    componentDidMount() {
    }

    // gets called just before navigating away from the route
    componentWillUnmount() {
    }

    onChangeAt = (i, j) => {
        return (e) => {
            let num = parseInt(e.target.value);
            if (isNaN(num)) num = 0;
            if (num < 0) num = 0;
            if (num > 9) num = 9;
            const data = this.state.data.slice();
            data[i][j] =  num;
            this.setState({ data });
        };
    };

    handleClick = () => {
        const table = this.state.data.map(row => row.map(cell => cell === "" ? "0" : cell).join("")).join("");
        axios.get('/solve?table=' + table).then(result => {
            if (result.data.status === 'ok')
                // this.setState({ data: result.data.result });
                alert(result.data.result);
            console.log(result.data);
        }).catch(err => {
            console.log(err);
            alert("something wrong");
        });
    }

    render({ }, { data }) {
        const range9 = [0,1,2,3,4,5,6,7,8];
        const listItems = range9.map((i) => {
            const line = range9.map((j) => (
                <td><input type="number" min="1" max="9" class={style.cell} value={data[i][j]} onChange={this.onChangeAt(i, j)} /></td>
            ));
            return <tr>{line}</tr>;
        });
        return (
            <div class={style.home}>
                <table>
                    {listItems}
                </table>
                <button onClick={this.handleClick}>Solve!</button>
            </div>
        );
    }
}
