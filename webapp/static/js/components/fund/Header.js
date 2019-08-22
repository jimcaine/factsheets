import React from 'react'

class Header extends React.Component {
  constructor() {
    super()
  }

  render() {
    return (
      <div>
        <h1 style={{'textAlign': 'center'}}>Fund: <span id="fund_name">{this.props.fundName}</span></h1>
        <hr/>
      </div>
    )
  }
}

export default Header