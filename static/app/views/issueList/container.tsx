import React, {Component} from 'react';
import DocumentTitle from 'react-document-title';

import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import GroupStore from 'app/stores/groupStore';
import {Organization, Project} from 'app/types';
import {callIfFunction} from 'app/utils/callIfFunction';
import withOrganization from 'app/utils/withOrganization';
import SampleEventAlert from 'app/views/organizationGroupDetails/sampleEventAlert';

type Props = {
  organization: Organization;
  projects: Project[];
};

class IssueListContainer extends Component<Props> {
  state: {
    showSampleEventBanner: boolean;
  } = {
    showSampleEventBanner: false,
  };

  getTitle() {
    return `Issues - ${this.props.organization.slug} - Sentry`;
  }

  listener = GroupStore.listen(() => this.onGroupChange(), undefined);
  render() {
    const {organization, children} = this.props;
    return (
      <DocumentTitle title={this.getTitle()}>
        <React.Fragment>
          {this.state.showSampleEventBanner && <SampleEventAlert />}
          <GlobalSelectionHeader>
            <LightWeightNoProjectMessage organization={organization}>
              {children}
            </LightWeightNoProjectMessage>
          </GlobalSelectionHeader>
        </React.Fragment>
      </DocumentTitle>
    );
  }

  onGroupChange() {
    this.setState({
      // Only display
      showSampleEventBanner: GroupStore.getAllItemIds().length === 1,
    });
  }

  componentWillUnmount() {
    callIfFunction(this.listener);
  }
}
export default withOrganization(IssueListContainer);
export {IssueListContainer};
