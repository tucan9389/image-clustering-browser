import React, { Component } from "react";
import { Grid, Form, Pagination, Segment } from "semantic-ui-react";

export default class PaginationExampleCustomization extends Component {
  state = {
    activePage: 1,
    boundaryRange: 1,
    siblingRange: 1,
    showEllipsis: true,
    showFirstAndLastNav: true,
    showPreviousAndNextNav: true,
    totalPages: 7,
  };

  constructor(props) {
    super(props);

    this.updatePage(this.props.activePage, this.props.totalPages);
  }

  componentDidUpdate(prevProps) {
    if (
      prevProps.activePage !== this.props.activePage ||
      prevProps.totalPages !== this.props.totalPages
    ) {
      this.updatePage(this.props.activePage, this.props.totalPages);
    }
  }

  updatePage(activePage, totalPages) {
    console.log(activePage);
    console.log(totalPages);
    this.setState({ activePage, totalPages });
  }

  handleCheckboxChange = (e, { checked, name }) =>
    this.setState({ [name]: checked });

  handleInputChange = (e, { name, value }) => {
    this.setState({ [name]: value });
  };

  handlePaginationChange = (e, { activePage }) => {
    this.setState({ activePage });
    this.props.handlePaginationChange(activePage);
  };

  render() {
    const {
      activePage,
      boundaryRange,
      siblingRange,
      showEllipsis,
      showFirstAndLastNav,
      showPreviousAndNextNav,
      totalPages,
    } = this.state;

    return (
      <Grid columns={1}>
        <Grid.Column>
          <Pagination
            activePage={activePage}
            boundaryRange={boundaryRange}
            onPageChange={this.handlePaginationChange}
            size="mini"
            siblingRange={siblingRange}
            totalPages={totalPages}
            // Heads up! All items are powered by shorthands, if you want to hide one of them, just pass `null` as value
            ellipsisItem={showEllipsis ? undefined : null}
            firstItem={showFirstAndLastNav ? undefined : null}
            lastItem={showFirstAndLastNav ? undefined : null}
            prevItem={showPreviousAndNextNav ? undefined : null}
            nextItem={showPreviousAndNextNav ? undefined : null}
          />
        </Grid.Column>
      </Grid>
    );
  }
}
