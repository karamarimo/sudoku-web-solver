import { h, Component } from 'preact';
import style from './style';

export default class Sudoku extends Component {
    constructor() {
        super();

        const data = [];
        for (let i = 0; i < 9; i++) {
            let row = [];
            for (let j = 0; j < 9; j++) {
                row.push("");
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
            const data = this.state.data.slice();
            data[i][j] = e.target.value;
            this.setState({ data });
        };
    };

    render({ }, { data }) {
        const range9 = [0,1,2,3,4,5,6,7,8];
        const listItems = range9.map((i) => {
            const line = range9.map((j) => (
                <td><input class={style.cell} value={data[i][j]} onChange={this.onChangeAt(i, j)} /></td>
            ));
            return <tr>{line}</tr>;
        });
        return (
            <div class={style.home}>
                <table>
                    {listItems}
                </table>
            </div>
        );
    }
}
