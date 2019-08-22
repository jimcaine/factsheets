import React from 'react'
import axios from 'axios'
import { ReactTabulator } from 'react-tabulator'

import Sidebar from './Sidebar'
import Header from './Header'

class Fund extends React.Component {

  constructor() {
    super()

    // get fundName from link
    let fundName = window.location.href
    fundName = fundName.split('/').slice(-1)[0]
    fundName = decodeURIComponent(fundName)

    // set initial state
    this.state = {
      fundName: fundName,
      returns: []
    }

    this.handleUpdateDataClick = this.handleUpdateDataClick.bind(this)
    this.handleChange = this.handleChange.bind(this)
  }

  componentDidMount() {
    axios.get('/api/fund', {
      params: {
        'fund_name': this.state.fundName
      }
    })
      .then((response) => {
        const returns = response.data.returns
        returns.forEach((item, i) => {
          item.id = i
        })

        this.setState({
          'fundOverview': response.data.fund_overview,
          'returns': returns
        })
        console.log(this.state)
      })
  }

  handleUpdateDataClick() {
    // send axios request
    axios.put('/api/fund', {
      fund_name: this.state.fundName,
      fund_overview: this.state.fundOverview,
      returns: this.refs['returns-table'].props.data
    })
      .then((response) => {
        console.log('Updated fund')
        console.log(response)
      })
  }

  handleChange(event) {
    const { name, value, type, checked } = event.target
    type === 'checkbox' ? this.setState({ [name]: checked }) : this.setState({ [name]: value} )
  }

  render() {

    // define tabulator columns
    const columns = [
      {title:"Year", field:"year"},
      {title:"Month", field:"month"},
      {title:"Return", field:"return", editor:true}
    ]

    return (
      <div id="body">
        <Sidebar 
          fundName={this.state.fundName}
          fundOverview={this.state.fundOverview} />

        <div className="container-fluid">

          <div className="content">
            <Header
              fundName={this.state.fundName} />
            <div>
              <label>Fund Overview</label>
              <div className="form-group">
                <textarea
                  className="form-control"
                  rows="5"
                  name="fundOverview"
                  value={this.state.fundOverview}
                  onChange={this.handleChange}>
                </textarea>
              </div>

              <div>
                <label>Fund Performance</label>
                <ReactTabulator 
                  ref='returns-table'
                  columns={columns}
                  data={this.state.returns}
                  options={{'height': 200}} />
              </div>
              <br/>

              <button
                className="btn btn-primary"
                onClick={ () => this.handleUpdateDataClick() }>
                Update Data
              </button>

            </div>
          </div>
        </div>
      </div>
    )
  }
}

export default Fund