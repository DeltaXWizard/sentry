import styled from '@emotion/styled';

import Tooltip from 'app/components/tooltip';
import SvgIcon from 'app/icons/svgIcon';

import Icon from './icon';

type Props = Required<Pick<React.ComponentProps<typeof SvgIcon>, 'color'>> &
  React.ComponentProps<typeof Icon> & {
    description?: string;
    error?: boolean;
  };

function Type({type, color, description, error}: Props) {
  return (
    <Wrapper error={error}>
      <Tooltip title={description} disabled={!description}>
        <IconWrapper color={color}>
          <Icon type={type} />
        </IconWrapper>
      </Tooltip>
    </Wrapper>
  );
}

export default Type;

const Wrapper = styled('div')<Pick<Props, 'error'>>`
  display: flex;
  justify-content: center;
  position: relative;
  :before {
    content: '';
    display: block;
    width: 1px;
    top: 0;
    bottom: 0;
    left: 50%;
    transform: translate(-50%);
    position: absolute;
    background: ${p => (p.error ? p.theme.red300 : p.theme.innerBorder)};
  }
`;

const IconWrapper = styled('div')<Pick<Props, 'color'>>`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  color: ${p => p.theme.white};
  background: ${p => p.theme[p.color] ?? p.color};
  box-shadow: ${p => p.theme.dropShadowLightest};
  position: relative;
`;
